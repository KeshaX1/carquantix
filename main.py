from flask import Flask, redirect, url_for, session, request, render_template, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import json
import hashlib
import hmac
import ipaddress
import urllib.parse
import time
import secrets
import smtplib
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from car_data import load_cars

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None

# Load .env explicitly so it works even if the app is started from another directory
DOTENV_PATH = Path(__file__).with_name(".env")
load_dotenv(DOTENV_PATH, override=False)  # do not override Render env values

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")

oauth = OAuth(app)
# GOOGLE DISCOVERY URL (compulsory)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# GOOGLE OAUTH CONFIG
# Keep the app bootable even if Google OAuth env vars are missing
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

FACEBOOK_CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID", "")
FACEBOOK_CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET", "")

print(f"[init] .env path={DOTENV_PATH} exists={DOTENV_PATH.exists()}")
print(f"[init] GOOGLE_CLIENT_ID full={GOOGLE_CLIENT_ID}")
if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
    print("[init] Facebook client_id detected")
else:
    print("[init] Facebook client_id/secret not set; Facebook login disabled")
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v2/",
        client_kwargs={
            "scope": "openid email profile"
        }
    )
else:
    print("[init] Google client_id/secret not set; Google login disabled")

if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
        authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
        api_base_url='https://graph.facebook.com/v12.0/',
        client_kwargs={'scope': 'email'}
    )

def can_write_storage_path(path_obj):
    parent = path_obj.parent
    probe = parent / f".cq_write_test_{os.getpid()}"
    try:
        parent.mkdir(parents=True, exist_ok=True)
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError as exc:
        print(f"[fs] storage path unavailable for {path_obj}: {exc}")
        return False


def resolve_data_path(env_var_name, filename):
    fallback = Path(__file__).with_name(filename)
    explicit = (os.environ.get(env_var_name, "") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    data_dir = (os.environ.get("APP_DATA_DIR", "") or "").strip()
    if not data_dir:
        return fallback

    candidate = Path(data_dir).expanduser() / filename
    if candidate.exists():
        return candidate
    if fallback.exists():
        print(f"[fs] using local fallback for {filename}: {fallback}")
        return fallback
    if can_write_storage_path(candidate):
        return candidate
    print(f"[fs] falling back to local storage for {filename}: {fallback}")
    return fallback


def ensure_parent_dir(path_obj):
    path_obj.parent.mkdir(parents=True, exist_ok=True)


USERS_PATH = resolve_data_path("USERS_PATH", "users.json")
PENDING_PATH = resolve_data_path("PENDING_PATH", "pending_verifications.json")
PENDING_RESET_PATH = resolve_data_path("PENDING_RESET_PATH", "pending_resets.json")
COMMENTS_PATH = resolve_data_path("COMMENTS_PATH", "comments.json")
PENDING_EXPIRY_SECONDS = 600  # 10 minutes
LOGIN_MEDIA_DIR = Path(__file__).with_name("login logo")
STATIC_DIR = Path(__file__).with_name("static")
ADS_TXT_DIR = Path(__file__).with_name("ads.txt")
ICON_DIR = STATIC_DIR / "icon"
BASE_URL = os.environ.get("BASE_URL", "https://carquantix.com").rstrip("/")
if not re.match(r"^https?://", BASE_URL):
    BASE_URL = f"https://{BASE_URL.lstrip('/')}"
_BASE_URL_PARTS = urllib.parse.urlparse(BASE_URL)
CANONICAL_SCHEME = (_BASE_URL_PARTS.scheme or "https").lower()
CANONICAL_HOST = (_BASE_URL_PARTS.netloc or "carquantix.com").lower()
CANONICAL_BASE_URL = f"{CANONICAL_SCHEME}://{CANONICAL_HOST}"
PADDLE_ENV = os.environ.get("PADDLE_ENV", "sandbox").strip().strip('"').strip("'").lower()
PADDLE_API_KEY = os.environ.get("PADDLE_API_KEY", "").strip()
PADDLE_PRICE_ID = os.environ.get("PADDLE_PRICE_ID", "").strip()
PADDLE_WEBHOOK_SECRET = os.environ.get("PADDLE_WEBHOOK_SECRET", "").strip()
PADDLE_CLIENT_TOKEN = os.environ.get("PADDLE_CLIENT_TOKEN", "").strip()
PADDLE_API_BASE = "https://api.paddle.com" if PADDLE_ENV == "production" else "https://sandbox-api.paddle.com"
PREMIUM_ACTIVE_STATUSES = {"active", "trialing"}
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
DB_CONNECT_TIMEOUT_SECONDS = int(os.environ.get("DB_CONNECT_TIMEOUT_SECONDS", "5"))
DB_RUNTIME_DISABLED = False
DB_BOOTSTRAP_ATTEMPTED = False
DB_BOOTSTRAP_IN_PROGRESS = False

FEATURED_CAR_SLUGS = [
    "2022-bmw-m5",
    "2024-bmw-xm",
    "2024-audi-a3",
    "2024-audi-a8",
    "2025-mercedes-benz-maybach-s-klasse",
    "2025-aston-martin-db",
    "2025-dodge-charger",
    "2018-dodge-demon",
    "2004-ferrari-enzo-ferrari",
    "2020-ford-mustang",
]
FEATURED_CAR_LIMIT = int(os.environ.get("FEATURED_CAR_LIMIT", "10"))
CURATED_COMPARE_REFERENCES = [
    ("M5", "RS6"),
    ("M8", "AMG GT"),
    ("RS7", "GT-R"),
    ("Panamera", "M8"),
    ("C8", "911 Turbo"),
    ("M5", "M8"),
    ("M5", "AMG GT"),
    ("RS7", "911 Turbo"),
    ("Panamera", "AMG GT"),
    ("Panamera", "911 Turbo"),
    ("M8", "911 Turbo"),
    ("X5", "GLS"),
    ("Q8", "GLS"),
    ("C8", "Huracan"),
    ("GT-R", "720S"),
]
FEATURED_COMPARE_REFERENCES = CURATED_COMPARE_REFERENCES + [
    ("M8", "R8"),
    ("M2", "TT RS"),
    ("Z4", "TT RS"),
    ("i4", "e-tron GT"),
    ("iX", "e-tron"),
    ("X6 M", "RS Q8"),
    ("XM", "SQ8"),
    ("550", "A6"),
    ("420", "A5"),
    ("320", "A4"),
    ("M3", "RS5"),
    ("M3", "C 63 AMG 2"),
    ("M3", "CT4"),
    ("M3", "Giulia"),
    ("M3", "Model Y"),
    ("RS5", "C 63 AMG 2"),
    ("RS5", "M4"),
    ("RS5", "Panamera"),
    ("RS5", "Model S"),
    ("RS5", "M5"),
    ("C 63 AMG 2", "M5"),
    ("C 63 AMG 2", "RS7"),
    ("C 63 AMG 2", "Model Y"),
    ("C 63 AMG 2", "Giulia"),
    ("C 63 AMG 2", "Panamera"),
    ("M5", "RS7"),
    ("M5", "E 53 AMG"),
    ("M5", "Panamera"),
    ("M5", "Model S"),
    ("M5", "CT5"),
    ("RS7", "Panamera"),
    ("RS7", "Model S"),
    ("RS7", "M8"),
    ("RS7", "AMG GT"),
    ("RS7", "M5 CS"),
    ("i4", "Model S"),
    ("i4", "1"),
    ("Model Y", "320"),
    ("Model Y", "A4"),
    ("Model Y", "C 63 AMG"),
    ("i4", "Model Y"),
    ("i4", "3"),
    ("i4", "4"),
    ("i4", "IONIQ 5"),
    ("i4", "EV6"),
    ("CT4", "M3"),
    ("CT4", "RS5"),
    ("CT4", "C 63 AMG 2"),
    ("CT5", "M5"),
    ("CT5", "RS7"),
    ("Giulia", "M3"),
    ("Giulia", "C 63 AMG 2"),
    ("Giulia", "RS4"),
    ("Giulia", "320"),
    ("Giulia", "C 63 AMG"),
    ("M3", "RS4"),
    ("M3", "C 63 AMG"),
    ("RS4", "C 63 AMG 2"),
    ("RS6", "550"),
    ("E 53 AMG", "550"),
    ("RS6", "M5 CS"),
    ("Giulia", "CT4"),
    ("CT5", "E 53 AMG"),
    ("Panamera", "M5 CS"),
    ("AMG GT", "911 Turbo"),
    ("GT-R", "911 Turbo"),
    ("R8", "AMG GT"),
    ("X5", "Q8"),
    ("X7", "GLS"),
    ("Range Rover", "Escalade"),
    ("911", "GT-R"),
    ("911", "R8"),
    ("911", "C8"),
    ("911", "M4"),
    ("911", "F-Type"),
    ("GT-R", "R8"),
    ("GT-R", "C8"),
    ("GT-R", "718 Cayman"),
    ("GT-R", "M8"),
    ("GT-R", "Huracan"),
    ("C8", "911"),
    ("C8", "GT-R"),
    ("C8", "R8"),
    ("C8", "Supra"),
    ("C8", "M4"),
    ("Huracan", "488"),
    ("Huracan", "720S"),
    ("Huracan", "R8"),
    ("Huracan", "F8"),
    ("Huracan", "911 Turbo"),
    ("488", "720S"),
    ("488", "Huracan"),
    ("488", "911 Turbo"),
    ("488", "R8"),
    ("488", "C8"),
    ("720S", "F8"),
    ("720S", "Huracan"),
    ("720S", "488"),
    ("720S", "911 Turbo"),
    ("720S", "R8"),
    ("718 Cayman", "Supra"),
    ("718 Cayman", "Z4"),
    ("718 Cayman", "TTS"),
    ("718 Cayman", "Nissan Z"),
    ("718 Cayman", "A110"),
    ("Supra", "Nissan Z"),
    ("Supra", "Z4"),
    ("Supra", "Mustang"),
    ("Supra", "Camaro SS"),
    ("Supra", "718 Cayman"),
    ("Z4", "TTS"),
    ("Z4", "718 Boxster"),
    ("Z4", "SLC"),
    ("Z4", "Supra"),
    ("Z4", "Nissan Z"),
    ("R8", "911"),
    ("R8", "Huracan"),
    ("R8", "488"),
    ("R8", "720S"),
    ("R8", "C8"),
    ("X5", "Q7"),
    ("X5", "GLE"),
    ("X5", "Cayenne"),
    ("X5", "Range Rover Sport"),
    ("X5", "Model X"),
    ("Q7", "GLE"),
    ("Q7", "X7"),
    ("Q7", "XC90"),
    ("Q7", "RX"),
    ("Q7", "MDX"),
    ("GLE", "X5"),
    ("GLE", "Q7"),
    ("GLE", "Cayenne"),
    ("GLE", "Range Rover"),
    ("GLE", "XC90"),
    ("Cayenne", "X5"),
    ("Cayenne", "Q8"),
    ("Cayenne", "Range Rover Sport"),
    ("Cayenne", "Urus"),
    ("Cayenne", "Levante"),
    ("Model X", "iX"),
    ("Model X", "e-tron"),
    ("Model X", "EQE SUV"),
    ("Model X", "R1S"),
    ("Model X", "Lyriq"),
    ("Range Rover", "GLS"),
    ("Range Rover", "X7"),
    ("Range Rover", "LX"),
    ("Range Rover", "Land Cruiser"),
    ("Range Rover", "Cayenne"),
    ("X3", "Q5"),
    ("X3", "GLC"),
    ("X3", "XC60"),
    ("X3", "NX"),
    ("X3", "RDX"),
    ("Q5", "GLC"),
    ("Q5", "X3"),
    ("Q5", "XC60"),
    ("Q5", "NX"),
    ("Q5", "Stelvio"),
    ("GLC", "X3"),
    ("GLC", "Q5"),
    ("GLC", "XC60"),
    ("GLC", "NX"),
    ("GLC", "RDX"),
    ("Urus", "Cayenne"),
    ("Urus", "DBX"),
    ("Urus", "Purosangue"),
    ("Urus", "Bentayga"),
    ("Urus", "Levante"),
    ("Taycan", "Model S"),
    ("Air", "Taycan"),
    ("IONIQ 5", "EV6"),
    ("GR86", "BRZ"),
    ("M2", "RS3"),
    ("Revuelto", "SF90 Spider"),
    ("Urus", "RS Q8"),
    ("Escalade", "GLS"),
    ("Model X", "EX90"),
    ("Artura", "911 Turbo"),
    ("Model Y", "Mustang Mach-E"),
    ("Model Y", "EV6"),
    ("Model Y", "IONIQ 5"),
    ("Enzo Ferrari", "Countach"),
    ("Enzo Ferrari", "Aventador"),
    ("Enzo Ferrari", "Revuelto"),
    ("Enzo Ferrari", "Sian FKP 37"),
    ("Enzo Ferrari", "Veneno"),
    ("LaFerrari", "Revuelto"),
    ("LaFerrari", "Sian FKP 37"),
    ("F40", "Countach 2"),
    ("F50", "Diablo"),
    ("F8", "Huracan"),
    ("Aventador", "Chiron"),
    ("Aventador", "Agera"),
    ("Chiron", "Veneno"),
    ("Huayra", "Aventador"),
    ("DB", "Roma"),
    ("F-Type", "Mustang"),
    ("Charger", "Demon"),
    ("AMG ONE", "Revuelto"),
    ("Temerario", "296"),
    ("12 Cilindri", "Vanquish"),
    ("GT2 Stradale", "911 Turbo"),
    ("Cybertruck", "R1S"),
    ("SU7", "Taycan"),
    ("Eletre", "RS Q8"),
    ("EV3", "EX30"),
    ("EV4", "ID.7"),
    ("Corvette", "911 Turbo"),
]
FEATURED_COMPARE_LIMIT = int(os.environ.get("FEATURED_COMPARE_LIMIT", str(len(FEATURED_COMPARE_REFERENCES))))
COMPARE_RACE_VIDEO_OVERRIDES = {}
LEGACY_COMPARE_SLUGS = {
    "audi-rs6-vs-bmw-m5-cs": ("RS6", "M5 CS"),
    "bugatti-chiron-vs-koenigsegg-agera-rs": ("Chiron", "Agera RS"),
    "ferrari-enzo-vs-lamborghini-countach": ("Enzo Ferrari", "Countach"),
    "ferrari-enzo-ferrari-vs-lamborghini-countach": ("Enzo Ferrari", "Countach"),
    "ferrari-enzo-vs-lamborghini-aventador": ("Enzo Ferrari", "Aventador"),
    "ferrari-enzo-vs-lamborghini-revuelto": ("Enzo Ferrari", "Revuelto"),
    "ferrari-laferrari-vs-lamborghini-revuelto": ("LaFerrari", "Revuelto"),
    "ferrari-f40-vs-lamborghini-countach": ("F40", "Countach 2"),
    "ferrari-f50-vs-lamborghini-diablo": ("F50", "Diablo"),
    "lamborghini-veneno-vs-ferrari-enzo-ferrari": ("Veneno", "Enzo Ferrari"),
    "mercedes-benz-sls-vs-aston-martin-lagonda": ("SLS", "Lagonda"),
    "pagani-huayra-vs-mclaren-720s": ("Huayra", "720S"),
}

SEO_SLUGS = {
    "audi-sq8-2024-fuel-cost",
    "tesla-model-y-charging-cost",
    "bmw-m5-fuel-consumption",
    "toyota-corolla-fuel-cost",
    "ford-mustang-mach-e-fuel-cost",
    "lamborghini-aventador-top-speed",
    "bmw-m5-top-speed",
    "bmw-m5-cs-top-speed",
    "audi-rs6-top-speed",
    "porsche-911-turbo-top-speed",
    "mercedes-amg-gt-top-speed",
}

DEFAULT_COMMENTS = [
    {"id": "seed_10", "username": "Ava S.", "text": "Good experience overall. It is easy to jump between models and compare specs without unnecessary clutter.", "rating": 4, "date": "12/03/2026", "likes": []},
    {"id": "seed_9", "username": "Noah G.", "text": "The interface is simple, dark theme looks solid, and the main metrics I care about are all visible.", "rating": 5, "date": "11/03/2026", "likes": []},
    {"id": "seed_8", "username": "Isabella N.", "text": "Helpful for quick research before watching review videos. I found the comparison table practical and clear.", "rating": 4, "date": "10/03/2026", "likes": ["seed_like_1", "seed_like_2"]},
    {"id": "seed_7", "username": "Ryan P.", "text": "Nice project. Search works well and the comment area makes the page feel more active.", "rating": 5, "date": "09/03/2026", "likes": []},
    {"id": "seed_6", "username": "Chloe B.", "text": "I was mainly looking at SUVs and this made it much easier to compare top speed and price in one place.", "rating": 4, "date": "08/03/2026", "likes": []},
    {"id": "seed_5", "username": "Marcus L.", "text": "The site is straightforward and the data cards are readable on desktop. Performance comparisons are especially nice.", "rating": 5, "date": "07/03/2026", "likes": ["seed_like_3", "seed_like_4", "seed_like_5"]},
    {"id": "seed_4", "username": "Olivia T.", "text": "Good design and simple navigation. The featured comparison links helped me discover cars I had not considered.", "rating": 4, "date": "06/03/2026", "likes": ["seed_like_6"]},
    {"id": "seed_3", "username": "Daniel K.", "text": "I like how quickly I can compare horsepower and 0-100 times without opening ten different tabs.", "rating": 5, "date": "05/03/2026", "likes": ["seed_like_7", "seed_like_8"]},
    {"id": "seed_2", "username": "Sofia M.", "text": "The fuel cost part is useful and the overall site feels fast. I would love even more EV entries later on.", "rating": 4, "date": "05/03/2026", "likes": []},
    {"id": "seed_1", "username": "Ethan R.", "text": "Very clean comparison layout. I checked a few BMW and Audi models and the numbers were easy to compare.", "rating": 5, "date": "04/03/2026", "likes": ["seed_like_9"]},
]

COMPARE_COMMENT_SEEDS = [
    {
        "username": "Max Torque",
        "text": "This comparison is exactly what I needed. Seeing power, acceleration and price together makes the choice much clearer.",
        "rating": 5,
        "date": "14/03/2026",
    },
    {
        "username": "Car Guy 47",
        "text": "Nice matchup. The table makes it easy to see which car is stronger for performance and which one makes more sense for daily use.",
        "rating": 4,
        "date": "13/03/2026",
    },
    {
        "username": "Liam V.",
        "text": "I was checking these two models and this page saved time. The top speed and 0-100 numbers are very easy to compare.",
        "rating": 5,
        "date": "12/03/2026",
    },
    {
        "username": "Turbo Dad",
        "text": "Good comparison page. I like that the specs are direct and there is no extra clutter around the important numbers.",
        "rating": 4,
        "date": "11/03/2026",
    },
    {
        "username": "Jake Miles",
        "text": "Useful for quick research before watching long reviews. The winner highlights make the differences obvious.",
        "rating": 5,
        "date": "10/03/2026",
    },
    {
        "username": "V8 Enjoyer",
        "text": "The numbers are laid out cleanly. I can tell very quickly which one is the faster car and which one is the better buy.",
        "rating": 5,
        "date": "09/03/2026",
    },
    {
        "username": "Oscar Lane",
        "text": "I like these direct comparisons. Price, power and fuel use are all in the same place without having to search around.",
        "rating": 4,
        "date": "08/03/2026",
    },
    {
        "username": "Spec Hunter",
        "text": "This is the kind of page I check before arguing with friends about which car is actually quicker.",
        "rating": 5,
        "date": "07/03/2026",
    },
    {
        "username": "Noah Shift",
        "text": "Solid comparison. The acceleration difference stands out immediately, and the table is easy to read on desktop.",
        "rating": 4,
        "date": "06/03/2026",
    },
    {
        "username": "Garage Wizard",
        "text": "I came for the horsepower numbers and stayed for the clean layout. Pretty useful for quick car debates.",
        "rating": 5,
        "date": "05/03/2026",
    },
]

NEWS_LAST_VERIFIED = "2026-03-16"
NEWS_ITEMS = [
    {
        "date_iso": "2026-03-04",
        "category_en": "New model",
        "category_tr": "Yeni model",
        "title_en": "Range Rover unveils the Sport SV Ultimate Edition",
        "title_tr": "Range Rover, Sport SV Ultimate Edition modelini tanitti",
        "summary_en": "The UK-only flagship adds a 635 PS twin-turbo mild-hybrid V8, 3.7-second 0-60 mph performance and a tightly curated SV specification.",
        "summary_tr": "Birlesik Krallik'a ozel yeni versiyon, 635 PS twin-turbo mild-hybrid V8 motor, 3.7 saniyelik 0-60 mph verisi ve ozel SV donanimi ile duyuruldu.",
        "facts_en": [
            "Land Rover says the model uses a 635 PS, 750 Nm V8 mild-hybrid powertrain.",
            "Official pricing starts from GBP 145,995 on the road in the UK.",
        ],
        "facts_tr": [
            "Land Rover, modelin 635 PS ve 750 Nm ureten V8 mild-hybrid altyapi kullandigini acikladi.",
            "Resmi baslangic fiyati Birlesik Krallik'ta 145,995 GBP olarak verildi.",
        ],
        "source_name": "Land Rover Media Newsroom",
        "source_url": "https://media.landrover.com/en-gb/news/2026/03/range-rover-sport-sv-ultimate-edition-curated-performance-refined",
    },
    {
        "date_iso": "2026-01-30",
        "category_en": "Hypercar",
        "category_tr": "Hiper otomobil",
        "title_en": "Bugatti gives the F.K.P. Hommage its physical world premiere",
        "title_tr": "Bugatti, F.K.P. Hommage modelinin fiziksel dunya promiyerini yapti",
        "summary_en": "After a digital reveal on January 22, Bugatti presented the F.K.P. Hommage at Retromobile 2026 as the second creation from Programme Solitaire.",
        "summary_tr": "22 Ocak'taki dijital tanitimin ardindan Bugatti, F.K.P. Hommage'i Retromobile 2026'da Programme Solitaire serisinin ikinci otomobili olarak sergiledi.",
        "facts_en": [
            "Bugatti links the car to the 20th anniversary of the Veyron.",
            "The company says the display took place inside the new Ultimate Supercar Garage area at Retromobile 2026.",
        ],
        "facts_tr": [
            "Bugatti, bu ozel otomobili Veyron'un 20. yilina adiyor.",
            "Marka, sergilemenin Retromobile 2026 icindeki yeni Ultimate Supercar Garage alaninda yapildigini belirtiyor.",
        ],
        "source_name": "Bugatti Newsroom",
        "source_url": "https://newsroom.bugatti.com/press-releases/bugatti-fkp-hommage-celebrating-20-years-of-veyron",
    },
    {
        "date_iso": "2026-01-19",
        "category_en": "Motorsport",
        "category_tr": "Motor sporlari",
        "title_en": "Defender wins the Dakar Stock class on its debut",
        "title_tr": "Defender, Dakar Stock sinifini ilk denemesinde kazandi",
        "summary_en": "Defender Rally finished first and second in the 2026 Dakar Rally Stock class, giving the brand a class win in its first competitive Dakar outing.",
        "summary_tr": "Defender Rally, 2026 Dakar Rally'sinin Stock sinifinda birinci ve ikinci olarak markaya ilk yaris Dakar katiliminda sinif galibiyeti getirdi.",
        "facts_en": [
            "Land Rover says Rokas Baciuska and Oriol Vidal won with a total time of 58h 09m 45s.",
            "The winning Defender Dakar D7X-R is derived from the Defender OCTA.",
        ],
        "facts_tr": [
            "Land Rover'a gore Rokas Baciuska ve Oriol Vidal 58 saat 09 dakika 45 saniyelik toplam sureyle zafere ulasti.",
            "Kazanan Defender Dakar D7X-R, Defender OCTA temel alinarak gelistirildi.",
        ],
        "source_name": "Land Rover Media Newsroom",
        "source_url": "https://media.landrover.com/en-gb/news/2026/01/defender-rally-make-history-debut-dakar-victory",
    },
    {
        "date_iso": "2026-01-09",
        "category_en": "Electric SUV",
        "category_tr": "Elektrikli SUV",
        "title_en": "Jeep brings the new Compass line and Wagoneer S to Brussels",
        "title_tr": "Jeep, yeni Compass ailesi ve Wagoneer S'i Bruksel'e getirdi",
        "summary_en": "Jeep used the Brussels Motor Show to debut the Compass e-Hybrid Plug-In and Compass 4xe while showcasing the 600 hp electric Wagoneer S.",
        "summary_tr": "Jeep, Bruksel Otomobil Fuari'nda Compass e-Hybrid Plug-In ve Compass 4xe versiyonlarini tanitirken 600 bg'lik elektrikli Wagoneer S'i de vitrine cikardi.",
        "facts_en": [
            "Jeep says the Wagoneer S reaches 0-100 km/h in 3.5 seconds with 600 horsepower.",
            "The new Compass range adds electrified e-Hybrid Plug-In and 4xe variants.",
        ],
        "facts_tr": [
            "Jeep, Wagoneer S'in 600 beygir guc ve 3.5 saniyelik 0-100 km/s verisi sundugunu acikladi.",
            "Yeni Compass ailesine e-Hybrid Plug-In ve 4xe gibi elektrik destekli versiyonlar eklendi.",
        ],
        "source_name": "Stellantis Media / Jeep",
        "source_url": "https://www.media.stellantis.com/uk-en/jeep/press/jeep-debuts-the-all-new-compass-lineup-and-the-cutting-edge-wagoneer-s-at-the-brussels-motor-show-2026",
    },
    {
        "date_iso": "2026-01-09",
        "category_en": "Electric fastback",
        "category_tr": "Elektrikli fastback",
        "title_en": "Peugeot refreshes the 408 and expands E-408 EV features",
        "title_tr": "Peugeot, 408'i yeniledi ve E-408'in EV ozelliklerini genisletti",
        "summary_en": "The updated 408 range now spans electric, plug-in hybrid and mild-hybrid powertrains, while the E-408 adds Battery Preconditioning, V2L and Plug & Charge.",
        "summary_tr": "Guncellenen 408 ailesi elektrikli, plug-in hybrid ve mild-hybrid seceneklerle sunulurken E-408 tarafina Battery Preconditioning, V2L ve Plug & Charge eklendi.",
        "facts_en": [
            "Peugeot says the new 408 is the brand's first model with illuminated rear PEUGEOT lettering.",
            "The all-electric E-408 adds EV-focused charging and power-delivery functions.",
        ],
        "facts_tr": [
            "Peugeot, yeni 408'in aydinlatmali arka PEUGEOT yazisina sahip ilk marka modeli oldugunu soyluyor.",
            "Tam elektrikli E-408'e sarj ve enerji aktarimina odakli yeni fonksiyonlar eklendi.",
        ],
        "source_name": "Stellantis Media / Peugeot",
        "source_url": "https://www.media.stellantis.com/em-en/peugeot/press/the-new-peugeot-408-wow-certified",
    },
    {
        "date_iso": "2026-01-09",
        "category_en": "World premiere",
        "category_tr": "Dunya promiyeri",
        "title_en": "Opel premieres the new Astra and Astra Sports Tourer in Brussels",
        "title_tr": "Opel, yeni Astra ve Astra Sports Tourer'i Bruksel'de tanitti",
        "summary_en": "Opel opened 2026 with the world premiere of the new Astra family, bringing the illuminated Blitz, Intelli-Lux HD light and a longer-range Astra Electric.",
        "summary_tr": "Opel, 2026'ya yeni Astra ailesinin dunya promiyeri ile girdi; aydinlatmali Blitz, Intelli-Lux HD farlar ve daha uzun menzilli Astra Electric dikkat cekti.",
        "facts_en": [
            "Opel states the Astra Electric can reach up to 454 km of WLTP range.",
            "The updated Astra also brings Vehicle to Load capability for the first time.",
        ],
        "facts_tr": [
            "Opel, Astra Electric'in WLTP'ye gore 454 km'ye kadar menzil sundugunu belirtiyor.",
            "Guncellenen Astra, ilk kez Vehicle to Load ozelligi de getiriyor.",
        ],
        "source_name": "Stellantis Media / Opel",
        "source_url": "https://www.media.stellantis.com/em-en/opel/press/new-opel-astra-celebrates-world-premiere-at-brussels-motor-show",
    },
    {
        "date_iso": "2026-01-09",
        "category_en": "Auto show",
        "category_tr": "Otomobil fuari",
        "title_en": "Brussels Motor Show 2026 closes with strong attendance and premieres",
        "title_tr": "Brussels Motor Show 2026 guclu ziyaretci sayisi ve promiyerlerle kapandi",
        "summary_en": "The organizers say the 2026 Brussels Motor Show welcomed 349,775 visitors and hosted 11 world premieres alongside 18 European premieres.",
        "summary_tr": "Organizatorlere gore 2026 Brussels Motor Show, 349,775 ziyaretci agirladi; 11 dunya ve 18 Avrupa promiyerine sahne oldu.",
        "facts_en": [
            "FEBIAC reports more than 100 exhibitors, including 67 car brands and 28 motorcycle brands.",
            "The event also featured 67 Belgian premieres, including 12 motorcycles.",
        ],
        "facts_tr": [
            "FEBIAC, fuarda 67 otomobil ve 28 motosiklet markasi dahil 100'den fazla katilimci oldugunu acikladi.",
            "Etkinlikte 12 motosiklet dahil 67 Belcika promiyeri de yer aldi.",
        ],
        "source_name": "FEBIAC / Brussels Motor Show",
        "source_url": "https://autosalon.be/en/brussels-motor-show-in-2026",
    },
]

GUIDE_ITEMS = [
    {
        "slug": "choose-a-sports-car",
        "title_en": "How to choose a sports car",
        "title_tr": "Spor otomobil nasil secilir",
        "summary_en": "A simple framework for balancing power, weight, daily usability, maintenance cost and driving character before you buy.",
        "summary_tr": "Satın almadan once guc, agirlik, gunluk kullanim, bakim maliyeti ve surus karakteri arasinda denge kurmak icin basit bir rehber.",
        "points_en": [
            "Start with your real use case: weekend fun, daily drive or track days.",
            "Check running costs, not only sticker price.",
            "Compare weight, tires and braking hardware alongside horsepower.",
        ],
        "points_tr": [
            "Once gercek kullanim amacini belirle: hafta sonu keyfi, gunluk kullanim ya da pist.",
            "Sadece etiket fiyatina degil, kullanim maliyetine de bak.",
            "Beygir gucu kadar agirlik, lastik ve fren altyapisini da karsilastir.",
        ],
        "tag_en": "Buying guide",
        "tag_tr": "Satın alma rehberi",
    },
    {
        "slug": "what-is-horsepower",
        "title_en": "What is horsepower?",
        "title_tr": "Horsepower nedir",
        "summary_en": "Understand what horsepower measures, how it differs from torque and why power figures alone do not tell the whole performance story.",
        "summary_tr": "Horsepower kavraminin neyi olctugunu, torktan farkini ve tek basina neden tum performansi anlatmadigini ogren.",
        "points_en": [
            "Horsepower describes how quickly an engine can do work.",
            "Torque affects low-speed punch and drivability.",
            "Gearing, traction and weight can change real-world acceleration.",
        ],
        "points_tr": [
            "Horsepower, motorun isi ne kadar hizli yapabildigini anlatir.",
            "Tork, dusuk hizdaki cekisi ve surus hissini etkiler.",
            "Sanziman oranlari, tutus ve agirlik gercek hizlanmayi ciddi sekilde degistirir.",
        ],
        "tag_en": "Basics",
        "tag_tr": "Temel bilgiler",
    },
    {
        "slug": "how-to-compare-cars",
        "title_en": "How to compare cars",
        "title_tr": "Arabalar nasil karsilastirilir",
        "summary_en": "A practical checklist for comparing cars without getting lost in spec-sheet noise.",
        "summary_tr": "Teknik veri kalabaliginda kaybolmadan araba karsilastirmak icin pratik bir kontrol listesi.",
        "points_en": [
            "Compare vehicles in the same price band and body type first.",
            "Use 0-100 km/h, top speed, power-to-weight and consumption together.",
            "Always add ownership cost and resale assumptions to the comparison.",
        ],
        "points_tr": [
            "Ilk olarak ayni fiyat araligi ve ayni kasa tipindeki araclari eslestir.",
            "0-100 km/s, azami hiz, guc/agırlik ve tuketimi birlikte degerlendir.",
            "Karsilastirmaya mutlaka sahip olma maliyeti ve ikinci el varsayimi ekle.",
        ],
        "tag_en": "Comparison",
        "tag_tr": "Karsilastirma",
    },
    {
        "slug": "understanding-0-100",
        "title_en": "How to read 0-100 km/h times",
        "title_tr": "0-100 km/s verileri nasil okunur",
        "summary_en": "Why launch control, traction, tire choice and test conditions can make one acceleration figure look better than another.",
        "summary_tr": "Launch control, tutus, lastik secimi ve test kosullarinin hizlanma verilerini nasil etkiledigini aciklayan rehber.",
        "points_en": [
            "Factory figures are often recorded in ideal conditions.",
            "AWD and tire setup matter at least as much as engine output off the line.",
            "Look at repeatability, not only the best single run.",
        ],
        "points_tr": [
            "Fabrika verileri genelde ideal kosullarda olculur.",
            "Kalkista dort ceker ve lastik yapisi en az motor kadar etkilidir.",
            "Tek en iyi deneme yerine tekrar edilebilir sonuclara bak.",
        ],
        "tag_en": "Performance",
        "tag_tr": "Performans",
    },
    {
        "slug": "fuel-vs-hybrid-vs-ev",
        "title_en": "Fuel, hybrid or EV: which fits you?",
        "title_tr": "Benzinli, hibrit veya EV: hangisi sana uygun",
        "summary_en": "A buyer-friendly way to think about charging access, annual mileage, urban use and long-trip habits before choosing a powertrain.",
        "summary_tr": "Guc secimini yapmadan once sarj erisimi, yillik kilometre, sehir ici kullanim ve uzun yol aliskanliklarini degerlendiren alici dostu bir rehber.",
        "points_en": [
            "EVs work best when charging is easy and predictable.",
            "Hybrids can reduce fuel use without changing habits much.",
            "Traditional combustion still suits some long-distance patterns.",
        ],
        "points_tr": [
            "Elektrikli araclar sarj kolay ve duzenliyse en iyi sonucu verir.",
            "Hibritler, aliskanliklari cok degistirmeden tuketimi dusurebilir.",
            "Klasik icten yanmali araclar bazi uzun yol duzenlerinde hala mantikli olabilir.",
        ],
        "tag_en": "Powertrain",
        "tag_tr": "Guc sistemi",
    },
    {
        "slug": "ownership-cost",
        "title_en": "How to estimate ownership cost",
        "title_tr": "Sahip olma maliyeti nasil hesaplanir",
        "summary_en": "Go beyond fuel with insurance, tires, servicing, depreciation and financing when comparing two cars.",
        "summary_tr": "Iki araci karsilastirirken yakitin disinda sigorta, lastik, servis, deger kaybi ve finansmani da hesaba kat.",
        "points_en": [
            "Create a yearly budget instead of a one-time purchase view.",
            "Large wheels, performance brakes and premium tires add hidden cost.",
            "Depreciation often matters more than small fuel savings.",
        ],
        "points_tr": [
            "Tek seferlik satin alma yerine yillik butce mantigi kur.",
            "Buyuk jant, performans frenleri ve premium lastikler gizli maliyet yaratir.",
            "Cogu zaman deger kaybi, kucuk yakit tasarrufundan daha belirleyicidir.",
        ],
        "tag_en": "Cost",
        "tag_tr": "Maliyet",
    },
]

BLOG_ITEMS = [
    {
        "slug": "fastest-cars-in-2026",
        "title_en": "Fastest cars people still talk about in 2026",
        "title_tr": "2026'da hala en cok konusulan hiz canavarlari",
        "summary_en": "A broad editorial look at the hypercars and high-speed benchmarks that continue to shape conversations this year.",
        "summary_tr": "Bu yil da otomobil sohbetlerini belirleyen hiper otomobillere ve yuksek hiz referanslarina genel bir editor bakisi.",
        "tag_en": "Speed",
        "tag_tr": "Hiz",
    },
    {
        "slug": "best-sports-cars-under-50k",
        "title_en": "Best sports cars under $50k: what buyers really compare",
        "title_tr": "50 bin dolar alti spor otomobillerde alicilar gercekte neyi karsilastiriyor",
        "summary_en": "Not a simple ranking, but a breakdown of the tradeoffs that matter most in the lower performance segment.",
        "summary_tr": "Basit bir siralama yerine, ulasilabilir performans sinifinda en cok onem tasiyan denge noktalarini ele alan yazi.",
        "tag_en": "Buying",
        "tag_tr": "Satın alma",
    },
    {
        "slug": "why-evs-are-growing",
        "title_en": "Why electric cars are becoming more popular",
        "title_tr": "Elektrikli araclar neden daha populer hale geliyor",
        "summary_en": "An accessible overview of convenience, software, efficiency and regulation factors behind EV adoption.",
        "summary_tr": "Elektrikli arac benimsenmesini etkileyen kolaylik, yazilim, verimlilik ve regülasyon dinamiklerine sade bir bakis.",
        "tag_en": "EV",
        "tag_tr": "EV",
    },
    {
        "slug": "super-sedan-vs-coupe",
        "title_en": "Super sedan vs coupe: which one makes more sense?",
        "title_tr": "Super sedan mi coupe mi: hangisi daha mantikli",
        "summary_en": "Practicality, weight distribution, comfort and image all shape this debate more than lap times alone.",
        "summary_tr": "Bu tartismayi sadece tur zamani degil; pratiklik, agirlik dagilimi, konfor ve imaj da belirliyor.",
        "tag_en": "Comparison",
        "tag_tr": "Karsilastirma",
    },
    {
        "slug": "digital-cockpit-trend",
        "title_en": "Why modern dashboards feel more digital every year",
        "title_tr": "Modern kokpitler neden her yil daha dijital hissediliyor",
        "summary_en": "A short read on software-first interiors, display design and the balance between simplicity and distraction.",
        "summary_tr": "Yazilim odakli kokpitler, ekran tasarimi ve sadelikle dikkat daginikligi arasindaki denge uzerine kisa bir yazi.",
        "tag_en": "Tech",
        "tag_tr": "Teknoloji",
    },
    {
        "slug": "why-weight-matters",
        "title_en": "Why weight matters almost as much as horsepower",
        "title_tr": "Neden agirlik neredeyse horsepower kadar onemlidir",
        "summary_en": "Handling, braking, efficiency and tire wear all reveal why lightness still matters in a power-focused market.",
        "summary_tr": "Yol tutus, fren, verimlilik ve lastik asinmasi; guce odakli pazarda hafifligin neden hala kritik oldugunu gosteriyor.",
        "tag_en": "Engineering",
        "tag_tr": "Muhendislik",
    },
]


def is_local_host(host):
    host_only = (host or "").split(":")[0].lower()
    if host_only in {"127.0.0.1", "localhost", "::1", "0.0.0.0"}:
        return True
    try:
        ipaddress.ip_address(host_only)
        return True
    except ValueError:
        return False


def is_platform_internal_host(host):
    host_only = (host or "").split(":")[0].lower()
    return (
        host_only.endswith(".onrender.com")
        or host_only.endswith(".internal")
        or "." not in host_only
    )


def get_forwarded_value(header_value, fallback):
    value = header_value or fallback or ""
    return value.split(",")[0].strip()


def format_display_price(value):
    raw = str(value or "").strip()
    if not raw:
        return "-"
    symbol_match = re.search(r"[€$£¥]", raw)
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return raw
    amount = f"{int(digits):,}"
    return f"{symbol_match.group(0)}{amount}" if symbol_match else amount


def build_car_specs(car):
    specs = []
    power = car.get("power")
    if power is not None:
        specs.append({"label": "Power", "value": f"{power} hp"})
    acc = car.get("acc")
    if acc is not None:
        specs.append({"label": "0-100 km/h", "value": f"{acc} s"})
    top_speed = car.get("topSpeed")
    if top_speed is not None:
        specs.append({"label": "Top Speed", "value": f"{top_speed} km/h"})
    engine = car.get("engine")
    if engine:
        specs.append({"label": "Engine", "value": engine})
    price = car.get("price")
    if price:
        specs.append({"label": "Price", "value": format_display_price(price)})
    consumption = car.get("consumption") or {}
    if consumption.get("value") is not None and consumption.get("unit"):
        specs.append(
            {
                "label": "Consumption",
                "value": f"{consumption['value']} {consumption['unit']}",
            }
        )
    return specs


def build_car_meta_description(car):
    bits = []
    if car.get("power") is not None:
        bits.append(f"{car['power']} hp")
    if car.get("acc") is not None:
        bits.append(f"0-100 km/h {car['acc']} s")
    if car.get("topSpeed") is not None:
        bits.append(f"Top speed {car['topSpeed']} km/h")
    if car.get("engine"):
        bits.append(car["engine"])
    summary = ", ".join(bits[:4])
    if summary:
        return f"{car.get('name', 'Car')} specs and details: {summary}."
    return f"{car.get('name', 'Car')} specs and details."


def get_base_url():
    scheme = get_forwarded_value(request.headers.get("X-Forwarded-Proto"), request.scheme or "https").lower()
    host = get_forwarded_value(request.headers.get("X-Forwarded-Host"), request.host)
    if is_local_host(host) or is_platform_internal_host(host):
        return f"{scheme}://{host}".rstrip("/")
    return CANONICAL_BASE_URL


def build_car_links(cars):
    return [
        {
            "name": car.get("name") or car.get("id") or car.get("slug") or "Car",
            "slug": car.get("slug"),
        }
        for car in cars
        if car.get("slug")
    ]


def select_featured_car_links(car_links):
    if FEATURED_CAR_SLUGS:
        index = {car["slug"]: car for car in car_links}
        featured = [index[slug] for slug in FEATURED_CAR_SLUGS if slug in index]
        if featured:
            return featured[:FEATURED_CAR_LIMIT]
    return car_links[:FEATURED_CAR_LIMIT]


def resolve_car_reference(reference, cars, slug_map):
    token = str(reference or "").strip().lower()
    if not token:
        return None
    direct = slug_map.get(token)
    if direct:
        return direct
    for car in cars:
        car_slug = str(car.get("slug") or "").strip().lower()
        car_id = str(car.get("id") or "").strip().lower()
        car_name = str(car.get("name") or "").strip().lower()
        if token in {car_slug, car_id, car_name}:
            return car
    return None


def slugify_compare_token(value):
    raw = str(value or "").strip().lower()
    raw = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return raw


def build_compare_car_token(car):
    base_slug = str(car.get("slug") or "").strip().lower()
    id_slug = slugify_compare_token(car.get("id"))
    if not base_slug:
        return id_slug
    if not id_slug or id_slug in base_slug:
        return base_slug
    return f"{base_slug}-{id_slug}"


def compare_slug_candidates(car):
    candidates = []
    for value in (
        car.get("slug"),
        build_compare_car_token(car),
        car.get("id"),
        car.get("name"),
        f"{car.get('name') or ''} {car.get('id') or ''}",
    ):
        token = slugify_compare_token(value)
        if token and token not in candidates:
            candidates.append(token)
    return candidates


def canonicalize_compare_pair(car_a, car_b):
    if not car_a or not car_b:
        return None, None
    ordered = sorted(
        [car_a, car_b],
        key=lambda car: (
            str(car.get("name") or "").lower(),
            str(car.get("slug") or "").lower(),
        ),
    )
    return ordered[0], ordered[1]


def build_compare_slug(car_a, car_b):
    left, right = canonicalize_compare_pair(car_a, car_b)
    if not left or not right:
        return ""
    left_token = build_compare_car_token(left)
    right_token = build_compare_car_token(right)
    if not left_token or not right_token:
        return ""
    return f"{left_token}-vs-{right_token}"


def build_compare_href(car_a, car_b):
    slug = build_compare_slug(car_a, car_b)
    if not slug:
        return ""
    return f"/compare/{slug}"


def build_compare_youtube_search_query(car_a, car_b):
    left_name = str(car_a.get("name") or "Car A").strip()
    right_name = str(car_b.get("name") or "Car B").strip()
    return f"{left_name} vs {right_name} drag race"


def build_compare_race_link(car_a, car_b):
    if not car_a or not car_b:
        return None
    compare_slug = build_compare_slug(car_a, car_b)
    override = COMPARE_RACE_VIDEO_OVERRIDES.get(compare_slug) if compare_slug else None
    if override:
        return {
            "title": override.get("title") or f"{car_a.get('name')} vs {car_b.get('name')}",
            "youtube_url": override.get("youtube_url", ""),
            "cta_label": override.get("cta_label") or "Watch on YouTube",
            "description": override.get("description") or "Open the curated YouTube video for this matchup.",
            "source": "direct",
        }

    query = build_compare_youtube_search_query(car_a, car_b)
    return {
        "title": f"{car_a.get('name')} vs {car_b.get('name')}",
        "youtube_url": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}",
        "cta_label": "Search on YouTube",
        "description": "Open YouTube search results for head-to-head runs of this matchup.",
        "source": "search",
    }


def resolve_compare_slug(compare_slug, slug_map):
    slug_text = str(compare_slug or "").strip().lower()
    if not slug_text or "-vs-" not in slug_text:
        return None
    cars, _ = load_cars()
    left_slug, right_slug = slug_text.split("-vs-", 1)
    left_car = next((car for car in cars if left_slug in compare_slug_candidates(car)), None)
    right_car = next((car for car in cars if right_slug in compare_slug_candidates(car)), None)
    if not left_car or not right_car:
        return None
    canonical_slug = build_compare_slug(left_car, right_car)
    if not canonical_slug:
        return None
    left_car, right_car = canonicalize_compare_pair(left_car, right_car)
    return {
        "left_car": left_car,
        "right_car": right_car,
        "canonical_slug": canonical_slug,
    }


def build_compare_spec_rows(car_a, car_b):
    def metric_row(label, key, higher_is_better=True, formatter=None):
        left_value = car_a.get(key)
        right_value = car_b.get(key)
        winner = None
        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)) and left_value != right_value:
            if higher_is_better:
                winner = "left" if left_value > right_value else "right"
            else:
                winner = "left" if left_value < right_value else "right"
        return {
            "label": label,
            "left_value": formatter(left_value) if formatter else left_value,
            "right_value": formatter(right_value) if formatter else right_value,
            "winner": winner,
        }

    def estimated_dimensions(car):
        name = str(car.get("name") or "").lower()
        engine = str(car.get("engine") or "").lower()
        power = car.get("power") if isinstance(car.get("power"), (int, float)) else 0

        length, width, weight = 465, 184, 1580
        if re.search(r"smart|a1|mini|fiat 500|abarth|spring|microlino|ami|twingo|aygo|picanto", name):
            length, width, weight = 374, 169, 1040
        elif re.search(r"hatch|golf|a3|focus|civic|corolla|megane|i20|clio|polo|208|308", name):
            length, width, weight = 430, 179, 1360
        elif re.search(r"suv|x3|x5|x6|x7|q3|q5|q7|q8|rav4|cr-v|hr-v|range rover|land rover|defender|urus|cayenne|tiguan|captur|tucson|sportage|duster|forester|outback|yangwang|u9", name):
            length, width, weight = 485, 195, 2150
        elif re.search(r"truck|pickup|f-150|ram|silverado|ranger|hilux|tundra|cybertruck", name):
            length, width, weight = 565, 203, 2450
        elif re.search(r"van|minivan|sienna|odyssey|carnival|transporter|multivan", name):
            length, width, weight = 510, 198, 2150
        elif re.search(r"coupe|911|r8|amg gt|mustang|camaro|challenger|corvette|supra|z4|tt|chiron|bugatti|ferrari|lamborghini|mclaren|aston|bentley azure|wiesmann", name):
            length, width, weight = 455, 193, 1650
        elif re.search(r"limousine|maybach|phantom|ghost|a8|s-class|7 series|i7|flying spur", name):
            length, width, weight = 535, 195, 2250
        elif re.search(r"wagon|avant|touring|estate|allroad", name):
            length, width, weight = 490, 187, 1750

        if "kwh" in engine or re.search(r"tesla|byd|xpeng|zeekr|nio|lucid|rivian|polestar|vinfast|voyah", name):
            weight += 280
        if power >= 700:
            weight += 180
        elif power >= 450:
            weight += 90
        elif power <= 80:
            weight -= 220

        return {"length": length, "width": width, "weight": max(700, weight)}

    def dimension_row(label, key, unit):
        left_dimensions = car_a.get("dimensions") or {}
        right_dimensions = car_b.get("dimensions") or {}
        left_value = left_dimensions.get(key, estimated_dimensions(car_a).get(key))
        right_value = right_dimensions.get(key, estimated_dimensions(car_b).get(key))
        return {
            "label": label,
            "left_value": f"{left_value:g} {unit}" if isinstance(left_value, (int, float)) else "-",
            "right_value": f"{right_value:g} {unit}" if isinstance(right_value, (int, float)) else "-",
            "winner": None,
        }

    consumption_a = car_a.get("consumption") or {}
    consumption_b = car_b.get("consumption") or {}
    same_consumption_unit = consumption_a.get("unit") and consumption_a.get("unit") == consumption_b.get("unit")
    consumption_winner = None
    if same_consumption_unit:
        value_a = consumption_a.get("value")
        value_b = consumption_b.get("value")
        if isinstance(value_a, (int, float)) and isinstance(value_b, (int, float)) and value_a != value_b:
            consumption_winner = "left" if value_a < value_b else "right"

    return [
        metric_row("Power", "power", True, lambda value: f"{value} hp" if value is not None else "-"),
        metric_row("0-100 km/h", "acc", False, lambda value: f"{value} s" if value is not None else "-"),
        metric_row("Top Speed", "topSpeed", True, lambda value: f"{value} km/h" if value is not None else "-"),
        {
            "label": "Engine",
            "left_value": car_a.get("engine") or "-",
            "right_value": car_b.get("engine") or "-",
            "winner": None,
        },
        dimension_row("Length", "length", "cm"),
        dimension_row("Width", "width", "cm"),
        dimension_row("Weight", "weight", "kg"),
        {
            "label": "Price",
            "left_value": format_display_price(car_a.get("price")),
            "right_value": format_display_price(car_b.get("price")),
            "winner": None,
        },
        {
            "label": "Consumption",
            "left_value": (
                f"{consumption_a.get('value')} {consumption_a.get('unit')}"
                if consumption_a.get("value") is not None and consumption_a.get("unit")
                else "-"
            ),
            "right_value": (
                f"{consumption_b.get('value')} {consumption_b.get('unit')}"
                if consumption_b.get("value") is not None and consumption_b.get("unit")
                else "-"
            ),
            "winner": consumption_winner,
        },
    ]


def build_compare_meta_description(car_a, car_b):
    parts = []
    if car_a.get("power") is not None and car_b.get("power") is not None:
        parts.append(f"{car_a['power']} hp vs {car_b['power']} hp")
    if car_a.get("acc") is not None and car_b.get("acc") is not None:
        parts.append(f"0-100 km/h {car_a['acc']} s vs {car_b['acc']} s")
    if car_a.get("topSpeed") is not None and car_b.get("topSpeed") is not None:
        parts.append(f"{car_a['topSpeed']} km/h vs {car_b['topSpeed']} km/h")
    summary = ", ".join(parts[:3])
    if summary:
        return f"Compare {car_a.get('name', 'Car A')} vs {car_b.get('name', 'Car B')}: {summary}."
    return f"Compare {car_a.get('name', 'Car A')} vs {car_b.get('name', 'Car B')} on CarQuantix."


def build_compare_intro_content(car_a, car_b):
    if not car_a or not car_b:
        return None

    left_name = str(car_a.get("name") or "Car A").strip()
    right_name = str(car_b.get("name") or "Car B").strip()
    left_engine = str(car_a.get("engine") or "").strip()
    right_engine = str(car_b.get("engine") or "").strip()
    left_power = car_a.get("power")
    right_power = car_b.get("power")
    left_acc = car_a.get("acc")
    right_acc = car_b.get("acc")
    left_top_speed = car_a.get("topSpeed")
    right_top_speed = car_b.get("topSpeed")
    left_price = format_display_price(car_a.get("price"))
    right_price = format_display_price(car_b.get("price"))
    left_consumption = car_a.get("consumption") or {}
    right_consumption = car_b.get("consumption") or {}

    highlights = []
    if left_power is not None and right_power is not None:
        highlights.append(f"Power: {left_power} hp vs {right_power} hp")
    if left_acc is not None and right_acc is not None:
        highlights.append(f"0-100 km/h: {left_acc} s vs {right_acc} s")
    if left_top_speed is not None and right_top_speed is not None:
        highlights.append(f"Top speed: {left_top_speed} km/h vs {right_top_speed} km/h")

    stats_sentences = []
    if left_power is not None and right_power is not None:
        if left_power == right_power:
            stats_sentences.append(f"Both models are rated at {left_power} hp, so raw output is evenly matched.")
        else:
            power_leader = left_name if left_power > right_power else right_name
            stats_sentences.append(
                f"On power, {power_leader} leads the matchup with "
                f"{max(left_power, right_power)} hp against {min(left_power, right_power)} hp."
            )
    if left_acc is not None and right_acc is not None:
        if left_acc == right_acc:
            stats_sentences.append(f"Acceleration is identical too, with both cars reaching 0-100 km/h in {left_acc} seconds.")
        else:
            acc_leader = left_name if left_acc < right_acc else right_name
            stats_sentences.append(
                f"For 0-100 km/h, {acc_leader} is quicker at {min(left_acc, right_acc)} seconds versus {max(left_acc, right_acc)} seconds."
            )
    if left_top_speed is not None and right_top_speed is not None:
        if left_top_speed == right_top_speed:
            stats_sentences.append(f"Top speed is also tied, with both reaching {left_top_speed} km/h.")
        else:
            speed_leader = left_name if left_top_speed > right_top_speed else right_name
            stats_sentences.append(
                f"At the top end, {speed_leader} reaches {max(left_top_speed, right_top_speed)} km/h, compared with {min(left_top_speed, right_top_speed)} km/h."
            )

    engine_sentence = ""
    if left_engine and right_engine:
        engine_sentence = f"{left_name} uses {left_engine}, while {right_name} comes with {right_engine}."
    elif left_engine or right_engine:
        engine_owner = left_name if left_engine else right_name
        engine_value = left_engine or right_engine
        engine_sentence = f"Engine character still matters here, and {engine_owner} stands out with its {engine_value} setup."

    value_sentences = []
    if left_price != "-" and right_price != "-":
        if left_price == right_price:
            value_sentences.append(f"Pricing is closely aligned as well, with both listed around {left_price}.")
        else:
            value_sentences.append(
                f"Price can shift the answer depending on your budget: {left_name} is listed at {left_price}, while {right_name} comes in at {right_price}."
            )

    same_consumption_unit = left_consumption.get("unit") and left_consumption.get("unit") == right_consumption.get("unit")
    if same_consumption_unit and left_consumption.get("value") is not None and right_consumption.get("value") is not None:
        left_cons = left_consumption["value"]
        right_cons = right_consumption["value"]
        unit = left_consumption["unit"]
        if left_cons == right_cons:
            value_sentences.append(f"Efficiency is basically the same too, with both cars rated at {left_cons} {unit}.")
        else:
            efficiency_leader = left_name if left_cons < right_cons else right_name
            value_sentences.append(
                f"If running costs matter, {efficiency_leader} looks more efficient on paper at {min(left_cons, right_cons)} {unit} versus {max(left_cons, right_cons)} {unit}."
            )

    paragraph_one = (
        f"The {left_name} vs {right_name} comparison is built for drivers who want a direct side-by-side view before making a shortlist. "
        f"If you are asking which is better between {left_name} and {right_name}, this page brings the most important numbers together in one place, "
        "including horsepower, 0-100 km/h performance, top speed, engine details, price, and fuel consumption. "
        "Some matchups look obvious at first glance, but the better choice often changes once you compare acceleration, high-speed performance, and day-to-day costs in the same view. "
        "That makes it easier to separate headline speed from real-world value without jumping between multiple tabs."
    )

    paragraph_two_bits = stats_sentences[:3]
    if engine_sentence:
        paragraph_two_bits.append(engine_sentence)
    paragraph_two = " ".join(paragraph_two_bits) or (
        f"This matchup gives you a clean look at how {left_name} and {right_name} compare across the core specs that usually decide a purchase."
    )

    paragraph_three_bits = value_sentences[:2]
    paragraph_three_bits.append(
        "The full comparison table adds more context beyond the headline figures, so you can judge where the performance gap is meaningful and where the differences are smaller than expected."
    )
    paragraph_three_bits.append(
        f"Use the detailed table below to decide whether {left_name} or {right_name} is the better fit for your priorities, whether that means speed, character, efficiency, or overall value."
    )
    paragraph_three = " ".join(paragraph_three_bits)

    return {
        "heading": f"{left_name} vs {right_name}: which is better for your priorities?",
        "paragraphs": [paragraph_one, paragraph_two, paragraph_three],
        "highlights": highlights,
    }


def extract_model_year(car):
    name = str((car or {}).get("name") or "").strip()
    match = re.search(r"\b(19|20)\d{2}\b", name)
    return int(match.group(0)) if match else None


def compare_numeric_values(left_value, right_value, higher_is_better=True):
    if not isinstance(left_value, (int, float)) or not isinstance(right_value, (int, float)) or left_value == right_value:
        return None
    if higher_is_better:
        return "left" if left_value > right_value else "right"
    return "left" if left_value < right_value else "right"


def parse_price_amount(value):
    digits = re.sub(r"\D", "", str(value or "").strip())
    return int(digits) if digits else None


def join_compare_labels(items):
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def append_unique(items, value):
    if value and value not in items:
        items.append(value)


def build_compare_decision_data(car_a, car_b):
    if not car_a or not car_b:
        return None

    left_name = str(car_a.get("name") or "Car A").strip()
    right_name = str(car_b.get("name") or "Car B").strip()
    left_year = extract_model_year(car_a)
    right_year = extract_model_year(car_b)
    left_price_amount = parse_price_amount(car_a.get("price"))
    right_price_amount = parse_price_amount(car_b.get("price"))
    left_consumption = car_a.get("consumption") or {}
    right_consumption = car_b.get("consumption") or {}

    power_winner = compare_numeric_values(car_a.get("power"), car_b.get("power"), True)
    acc_winner = compare_numeric_values(car_a.get("acc"), car_b.get("acc"), False)
    top_speed_winner = compare_numeric_values(car_a.get("topSpeed"), car_b.get("topSpeed"), True)
    price_winner = compare_numeric_values(left_price_amount, right_price_amount, False)

    consumption_winner = None
    if (
        left_consumption.get("unit")
        and left_consumption.get("unit") == right_consumption.get("unit")
        and left_consumption.get("value") is not None
        and right_consumption.get("value") is not None
    ):
        consumption_winner = compare_numeric_values(left_consumption.get("value"), right_consumption.get("value"), False)

    year_winner = compare_numeric_values(left_year, right_year, True)

    performance_scores = {"left": 0, "right": 0}
    performance_labels = {"left": [], "right": []}
    for winner, label in (
        (power_winner, "power"),
        (acc_winner, "0-100 km/h"),
        (top_speed_winner, "top speed"),
    ):
        if winner:
            performance_scores[winner] += 1
            performance_labels[winner].append(label)

    if performance_scores["left"] > performance_scores["right"]:
        performance_winner = "left"
    elif performance_scores["right"] > performance_scores["left"]:
        performance_winner = "right"
    else:
        performance_winner = acc_winner or power_winner or top_speed_winner

    value_scores = {"left": 0, "right": 0}
    value_labels = {"left": [], "right": []}
    for winner, label in (
        (price_winner, "price"),
        (consumption_winner, "efficiency"),
        (year_winner, "model year"),
    ):
        if winner:
            value_scores[winner] += 1
            value_labels[winner].append(label)

    if value_scores["left"] > value_scores["right"]:
        value_winner = "left"
    elif value_scores["right"] > value_scores["left"]:
        value_winner = "right"
    else:
        value_winner = price_winner or consumption_winner or year_winner

    speed_winner = top_speed_winner or acc_winner or performance_winner

    overall_scores = {"left": 0, "right": 0}
    for winner in (power_winner, acc_winner, top_speed_winner, price_winner, consumption_winner, year_winner):
        if winner:
            overall_scores[winner] += 1
    if performance_winner:
        overall_scores[performance_winner] += 1
    if value_winner:
        overall_scores[value_winner] += 1
    if speed_winner:
        overall_scores[speed_winner] += 1

    if overall_scores["left"] > overall_scores["right"]:
        overall_winner = "left"
    elif overall_scores["right"] > overall_scores["left"]:
        overall_winner = "right"
    else:
        overall_winner = performance_winner or value_winner or speed_winner

    winner_name = {
        "left": left_name,
        "right": right_name,
        None: "Too close to call",
    }

    verdict_items = [
        {
            "label": "Performance winner",
            "winner": winner_name[performance_winner],
            "reason": (
                f"Leads on {join_compare_labels(performance_labels[performance_winner])}."
                if performance_winner and performance_labels[performance_winner]
                else "No clear edge on the recorded performance data."
            ),
        },
        {
            "label": "Speed winner",
            "winner": winner_name[speed_winner],
            "reason": (
                "Higher top speed on paper."
                if speed_winner and top_speed_winner == speed_winner
                else "Quicker acceleration on paper."
                if speed_winner and acc_winner == speed_winner
                else "No clear speed advantage on the recorded data."
            ),
        },
        {
            "label": "Value winner",
            "winner": winner_name[value_winner],
            "reason": (
                f"Stronger on {join_compare_labels(value_labels[value_winner])}."
                if value_winner and value_labels[value_winner]
                else "No clear value edge on price, efficiency, or model year."
            ),
        },
        {
            "label": "Overall winner",
            "winner": winner_name[overall_winner],
            "reason": (
                "Wins more of the recorded comparison categories overall."
                if overall_winner
                else "The available data is too evenly matched to separate them."
            ),
        },
    ]

    left_pros = []
    left_cons = []
    right_pros = []
    right_cons = []

    if power_winner == "left":
        append_unique(left_pros, "More power")
        append_unique(right_cons, "Less power")
    elif power_winner == "right":
        append_unique(right_pros, "More power")
        append_unique(left_cons, "Less power")

    if acc_winner == "left":
        append_unique(left_pros, "Quicker 0-100 km/h")
        append_unique(right_cons, "Slower off the line")
    elif acc_winner == "right":
        append_unique(right_pros, "Quicker 0-100 km/h")
        append_unique(left_cons, "Slower off the line")

    if top_speed_winner == "left":
        append_unique(left_pros, "Higher top speed")
        append_unique(right_cons, "Lower top speed")
    elif top_speed_winner == "right":
        append_unique(right_pros, "Higher top speed")
        append_unique(left_cons, "Lower top speed")

    if price_winner == "left":
        append_unique(left_pros, "Lower price")
        append_unique(right_cons, "Higher price")
    elif price_winner == "right":
        append_unique(right_pros, "Lower price")
        append_unique(left_cons, "Higher price")

    if consumption_winner == "left":
        append_unique(left_pros, "Better efficiency")
        append_unique(right_cons, "Higher fuel consumption")
    elif consumption_winner == "right":
        append_unique(right_pros, "Better efficiency")
        append_unique(left_cons, "Higher fuel consumption")

    if year_winner == "left":
        append_unique(left_pros, "Newer model year")
        append_unique(right_cons, "Older model year")
    elif year_winner == "right":
        append_unique(right_pros, "Newer model year")
        append_unique(left_cons, "Older model year")

    if not left_pros:
        append_unique(left_pros, "Competitive overall spec balance")
    if not right_pros:
        append_unique(right_pros, "Competitive overall spec balance")
    if not left_cons:
        append_unique(left_cons, "Few clear weaknesses in the recorded specs")
    if not right_cons:
        append_unique(right_cons, "Few clear weaknesses in the recorded specs")

    return {
        "verdict_items": verdict_items,
        "left": {
            "pros": left_pros[:3],
            "cons": left_cons[:3],
        },
        "right": {
            "pros": right_pros[:3],
            "cons": right_cons[:3],
        },
    }


def build_featured_compare_links(cars, slug_map):
    links = []
    seen = set()
    for left_ref, right_ref in FEATURED_COMPARE_REFERENCES:
        left_car = resolve_car_reference(left_ref, cars, slug_map)
        right_car = resolve_car_reference(right_ref, cars, slug_map)
        if not left_car or not right_car:
            continue
        href = build_compare_href(left_car, right_car)
        if not href or href in seen:
            continue
        seen.add(href)
        links.append(
            {
                "href": href,
                "title": f"{left_car.get('name')} vs {right_car.get('name')}",
                "left_car": left_car,
                "right_car": right_car,
            }
        )
        if len(links) >= FEATURED_COMPARE_LIMIT:
            break
    return links


@app.before_request
def enforce_canonical_origin():
    if request.method not in ("GET", "HEAD"):
        return None
    if request.path == "/health":
        return None
    scheme = get_forwarded_value(request.headers.get("X-Forwarded-Proto"), request.scheme or "https").lower()
    host = get_forwarded_value(request.headers.get("X-Forwarded-Host"), request.host).lower()
    host_only = host.split(":")[0]
    if is_local_host(host_only) or is_platform_internal_host(host_only):
        return None
    if scheme == CANONICAL_SCHEME and host_only == CANONICAL_HOST:
        return None
    target = f"{CANONICAL_BASE_URL}{request.path}"
    query_string = request.query_string.decode("utf-8")
    if query_string:
        target = f"{target}?{query_string}"
    return redirect(target, code=301)


@app.before_request
def sync_session_user_state():
    if request.path == "/health":
        return None
    refresh_session_user_from_store()


@app.after_request
def add_cache_headers(response):
    path = request.path or ""
    host = (request.host or "").lower()
    is_local = host.startswith(("127.0.0.1", "localhost"))
    if path.startswith("/static/") or path.startswith("/login-media/"):
        if is_local:
            response.cache_control.no_store = True
        else:
            response.cache_control.public = True
            response.cache_control.max_age = 31536000
            response.cache_control.immutable = True
    elif response.mimetype == "text/html":
        response.cache_control.no_store = True
    return response


def load_users():
    if not USERS_PATH.exists():
        return []
    try:
        return json.loads(USERS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_users(users):
    ensure_parent_dir(USERS_PATH)
    USERS_PATH.write_text(json.dumps(users, indent=2), encoding="utf-8")


def _generate_comment_id(prefix="c"):
    return f"{prefix}_{int(time.time() * 1000)}_{secrets.token_hex(4)}"


def _normalize_reply(reply):
    payload = dict(reply or {})
    username = str(payload.get("username") or "User").strip() or "User"
    text = str(payload.get("text") or "").strip()
    date = str(payload.get("date") or datetime.utcnow().strftime("%d/%m/%Y")).strip()
    user_id = str(payload.get("userId") or "").strip() or None
    return {
        "id": str(payload.get("id") or _generate_comment_id("r")).strip(),
        "username": username,
        "userId": user_id,
        "text": text,
        "date": date,
    }


def _normalize_comment(comment):
    payload = dict(comment or {})
    username = str(payload.get("username") or "User").strip() or "User"
    text = str(payload.get("text") or "").strip()
    date = str(payload.get("date") or datetime.utcnow().strftime("%d/%m/%Y")).strip()
    page = str(payload.get("page") or "home").strip() or "home"
    try:
        rating = int(payload.get("rating") or 5)
    except (TypeError, ValueError):
        rating = 5
    rating = max(1, min(5, rating))

    likes = payload.get("likes")
    if not isinstance(likes, list):
        likes = []
    likes = [str(value).strip() for value in likes if str(value).strip()]
    likes = list(dict.fromkeys(likes))

    dislikes = payload.get("dislikes")
    if not isinstance(dislikes, list):
        dislikes = []
    dislikes = [str(value).strip() for value in dislikes if str(value).strip()]
    dislikes = list(dict.fromkeys(dislikes))

    replies = payload.get("replies")
    if not isinstance(replies, list):
        replies = []

    user_id = str(payload.get("userId") or "").strip() or None

    return {
        "id": str(payload.get("id") or _generate_comment_id("c")).strip(),
        "username": username,
        "userId": user_id,
        "text": text,
        "page": page,
        "rating": rating,
        "date": date,
        "likes": likes,
        "dislikes": dislikes,
        "replies": [_normalize_reply(reply) for reply in replies],
    }


def _comment_seed_key(page):
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", str(page or "home")).strip("_")[:80] or "home"


def build_compare_seed_comments(page, existing_count=0):
    page = get_comment_page(page)
    if not page.startswith("compare:"):
        return []

    seed_key = _comment_seed_key(page)
    digest = hashlib.sha256(page.encode("utf-8")).digest()
    needed = max(0, 2 - int(existing_count or 0))
    comments = []
    for offset in range(needed):
        seed_index = digest[offset % len(digest)] % len(COMPARE_COMMENT_SEEDS)
        while any(item["username"] == COMPARE_COMMENT_SEEDS[seed_index]["username"] for item in comments):
            seed_index = (seed_index + 1) % len(COMPARE_COMMENT_SEEDS)
        template = COMPARE_COMMENT_SEEDS[seed_index]
        comments.append(
            _normalize_comment(
                {
                    **template,
                    "id": f"seed_{seed_key}_{offset + 1}",
                    "page": page,
                    "likes": [f"seed_like_{seed_key}_{offset + 1}"] if template["rating"] >= 5 else [],
                    "dislikes": [],
                    "replies": [],
                }
            )
        )
    return comments


def get_comments_for_page(page, comments=None):
    page = get_comment_page(page)
    source_comments = load_comments() if comments is None else comments
    page_comments = [comment for comment in source_comments if comment.get("page", "home") == page]
    existing_ids = {comment.get("id") for comment in page_comments}
    seed_comments = [
        comment for comment in build_compare_seed_comments(page, len(page_comments))
        if comment.get("id") not in existing_ids
    ]
    return page_comments + seed_comments


def load_comments():
    raw_comments = []
    if COMMENTS_PATH.exists():
        try:
            parsed = json.loads(COMMENTS_PATH.read_text(encoding="utf-8"))
            if isinstance(parsed, list):
                raw_comments = parsed
        except json.JSONDecodeError:
            raw_comments = []

    comments = []
    seen_ids = set()
    defaults_by_id = {item["id"]: _normalize_comment(item) for item in DEFAULT_COMMENTS}
    for item in raw_comments:
        normalized = _normalize_comment(item)
        if not normalized["text"] or normalized["id"] in seen_ids:
            continue
        default_version = defaults_by_id.get(normalized["id"])
        if default_version:
            if not normalized.get("likes") and default_version.get("likes"):
                normalized["likes"] = default_version["likes"][:]
            if not normalized.get("dislikes") and default_version.get("dislikes"):
                normalized["dislikes"] = default_version["dislikes"][:]
            if not normalized.get("replies") and default_version.get("replies"):
                normalized["replies"] = default_version["replies"][:]
        comments.append(normalized)
        seen_ids.add(normalized["id"])

    changed = comments != raw_comments
    for seed in DEFAULT_COMMENTS:
        normalized_seed = _normalize_comment(seed)
        if normalized_seed["id"] in seen_ids:
            continue
        comments.append(normalized_seed)
        seen_ids.add(normalized_seed["id"])
        changed = True

    if changed:
        save_comments(comments)
    return comments


def save_comments(comments):
    ensure_parent_dir(COMMENTS_PATH)
    COMMENTS_PATH.write_text(json.dumps(comments, indent=2), encoding="utf-8")


def get_comment_identity():
    user = session.get("user") or {}
    email = (user.get("email") or "").strip().lower()
    if not email:
        return None
    username = (user.get("name") or email).strip() or email
    return {"user_id": email, "username": username}


def get_comment_page(value=None):
    page = str(value or request.args.get("page") or "home").strip()
    if not page:
        return "home"
    page = re.sub(r"[^a-zA-Z0-9:_./-]+", "-", page)[:120].strip("-")
    return page or "home"


def db_enabled():
    return bool(DATABASE_URL and psycopg is not None and not DB_RUNTIME_DISABLED)


def disable_db_runtime(reason):
    global DB_RUNTIME_DISABLED
    if DB_RUNTIME_DISABLED:
        return
    DB_RUNTIME_DISABLED = True
    print(f"[db] runtime disabled: {reason}")


def ensure_db_ready():
    global DB_BOOTSTRAP_ATTEMPTED, DB_BOOTSTRAP_IN_PROGRESS
    if DB_BOOTSTRAP_ATTEMPTED or DB_BOOTSTRAP_IN_PROGRESS:
        return
    if not DATABASE_URL or psycopg is None or DB_RUNTIME_DISABLED:
        DB_BOOTSTRAP_ATTEMPTED = True
        return
    DB_BOOTSTRAP_IN_PROGRESS = True
    try:
        init_user_db()
        migrate_json_users_to_db()
    except Exception as exc:
        disable_db_runtime(f"bootstrap failed: {exc}")
    finally:
        DB_BOOTSTRAP_IN_PROGRESS = False
        DB_BOOTSTRAP_ATTEMPTED = True


def get_db_conn():
    if not db_enabled():
        return None
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
        connect_timeout=DB_CONNECT_TIMEOUT_SECONDS,
    )


def init_user_db():
    if not db_enabled():
        if DATABASE_URL and psycopg is None:
            print("[db] DATABASE_URL is set but psycopg is not installed; falling back to users.json")
        return
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id BIGSERIAL PRIMARY KEY,
                        email TEXT NOT NULL UNIQUE,
                        name TEXT,
                        picture TEXT,
                        password_hash TEXT,
                        provider TEXT,
                        subscription_status TEXT NOT NULL DEFAULT 'free',
                        subscription_expires_at TEXT,
                        subscription_updated_at BIGINT,
                        paddle_customer_id TEXT,
                        paddle_subscription_id TEXT,
                        paddle_last_transaction_id TEXT,
                        paddle_last_event_type TEXT,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
                cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users (lower(email))")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_users_paddle_customer_id ON users (paddle_customer_id)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_users_paddle_subscription_id ON users (paddle_subscription_id)")
            conn.commit()
    except Exception as exc:
        print(f"[db] init skipped; database unavailable: {exc}")
        disable_db_runtime(exc)


def count_db_users():
    if not db_enabled():
        return 0
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS count FROM users")
                row = cur.fetchone() or {}
                return int(row.get("count") or 0)
    except Exception as exc:
        print(f"[db] count skipped; database unavailable: {exc}")
        disable_db_runtime(exc)
        return 0


def get_smtp_config():
    host = os.environ.get("SMTP_HOST")
    port = os.environ.get("SMTP_PORT")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    sender = os.environ.get("SMTP_FROM") or user
    use_tls = os.environ.get("SMTP_USE_TLS", "1").lower() not in ("0", "false", "no")
    if not all([host, port, user, password, sender]):
        missing = []
        if not host: missing.append("SMTP_HOST")
        if not port: missing.append("SMTP_PORT")
        if not user: missing.append("SMTP_USER")
        if not password: missing.append("SMTP_PASSWORD")
        if not sender: missing.append("SMTP_FROM")
        print(f"[email] SMTP config missing keys={missing} host={host} port={port} user={user} sender={sender} password_len={len(password or '')}")
        return None
    try:
        port = int(port)
    except ValueError:
        port = 587
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": sender,
        "use_tls": use_tls,
    }


def send_verification_email(to_email, code):
    cfg = get_smtp_config()
    if not cfg:
        print("[email] SMTP config missing; skipping send.")
        return False, "SMTP configuration missing."
    subject = "Your verification code"
    body = f"Your verification code is {code}. It expires in 10 minutes."
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = cfg["sender"]
        msg["To"] = to_email
        msg.set_content(body)
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
            server.set_debuglevel(1)  # show SMTP conversation in terminal for troubleshooting
            if cfg["use_tls"]:
                server.starttls()
            server.login(cfg["user"], cfg["password"])
            server.send_message(msg)
        print(f"[email] verification code sent to {to_email}")
        return True, "sent"
    except Exception as exc:
        print(f"[email] failed to send to {to_email}: {exc}")
        return False, str(exc)


def send_reset_email(to_email, code):
    cfg = get_smtp_config()
    if not cfg:
        print("[email] SMTP config missing; skipping reset send.")
        return False, "SMTP configuration missing."
    subject = "Your password reset code"
    body = f"Your password reset code is {code}. It expires in 10 minutes."
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = cfg["sender"]
        msg["To"] = to_email
        msg.set_content(body)
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
            server.set_debuglevel(1)
            if cfg["use_tls"]:
                server.starttls()
            server.login(cfg["user"], cfg["password"])
            server.send_message(msg)
        print(f"[email] reset code sent to {to_email}")
        return True, "sent"
    except Exception as exc:
        print(f"[email] failed to send reset code to {to_email}: {exc}")
        return False, str(exc)


@app.route("/test-mail")
def test_mail():
    """Send a test email to the configured from-address to debug SMTP quickly."""
    target = os.environ.get("SMTP_TEST_TO") or os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER")
    code = generate_verification_code()
    ok, msg = send_verification_email(target, code)
    return jsonify({"ok": ok, "message": msg, "code": code, "target": target})


def load_pending():
    if not PENDING_PATH.exists():
        return {}
    try:
        data = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {}


def save_pending(data):
    ensure_parent_dir(PENDING_PATH)
    PENDING_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def prune_expired_pending():
    pending = load_pending()
    now = time.time()
    removed = False
    for email in list(pending.keys()):
        if pending[email].get("expires_at", 0) < now:
            pending.pop(email, None)
            removed = True
    if removed:
        save_pending(pending)
    return pending


def generate_verification_code():
    return f"{secrets.randbelow(1_000_000):06d}"


def load_reset_pending():
    if not PENDING_RESET_PATH.exists():
        return {}
    try:
        data = json.loads(PENDING_RESET_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {}


def save_reset_pending(data):
    ensure_parent_dir(PENDING_RESET_PATH)
    PENDING_RESET_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def prune_expired_reset_pending():
    pending = load_reset_pending()
    now = time.time()
    removed = False
    for email in list(pending.keys()):
        if pending[email].get("expires_at", 0) < now:
            pending.pop(email, None)
            removed = True
    if removed:
        save_reset_pending(pending)
    return pending


def find_user(email):
    if not email:
        return None
    email_l = email.lower()
    ensure_db_ready()
    if db_enabled():
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE lower(email) = %s LIMIT 1", (email_l,))
                    return cur.fetchone()
        except Exception as exc:
            print(f"[db] find_user fallback for {email_l}: {exc}")
            disable_db_runtime(exc)
    for u in load_users():
        if u.get("email", "").lower() == email_l:
            return u
    return None


def verify_password(stored_hash, candidate):
    # Support old plain sha256 hex hashes and werkzeug hashes
    if stored_hash.startswith(("pbkdf2:", "scrypt:", "bcrypt:")):
        return check_password_hash(stored_hash, candidate)
    if len(stored_hash) == 64:
        return hashlib.sha256(candidate.encode("utf-8")).hexdigest() == stored_hash
    return False


def letter_avatar(initial="U"):
    ch = (initial or "U")[0].upper()
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96"><rect width="100%" height="100%" rx="20" fill="#007bff"/><text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="48" font-family="Arial, sans-serif">{ch}</text></svg>'
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def find_user_index(users, email):
    target = (email or "").strip().lower()
    if not target:
        return None
    for idx, u in enumerate(users):
        if (u.get("email") or "").strip().lower() == target:
            return idx
    return None


def find_user_index_by_billing_ids(users, customer_id=None, subscription_id=None):
    customer_id = (customer_id or "").strip()
    subscription_id = (subscription_id or "").strip()
    if not customer_id and not subscription_id:
        return None
    for idx, u in enumerate(users):
        if customer_id and u.get("paddle_customer_id") == customer_id:
            return idx
        if subscription_id and u.get("paddle_subscription_id") == subscription_id:
            return idx
    return None


def find_user_by_billing_ids(customer_id=None, subscription_id=None):
    customer_id = (customer_id or "").strip()
    subscription_id = (subscription_id or "").strip()
    if not customer_id and not subscription_id:
        return None
    ensure_db_ready()
    if db_enabled():
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    if customer_id and subscription_id:
                        cur.execute(
                            """
                            SELECT * FROM users
                            WHERE paddle_customer_id = %s OR paddle_subscription_id = %s
                            LIMIT 1
                            """,
                            (customer_id, subscription_id),
                        )
                    elif customer_id:
                        cur.execute("SELECT * FROM users WHERE paddle_customer_id = %s LIMIT 1", (customer_id,))
                    else:
                        cur.execute("SELECT * FROM users WHERE paddle_subscription_id = %s LIMIT 1", (subscription_id,))
                    return cur.fetchone()
        except Exception as exc:
            print(f"[db] billing lookup fallback: {exc}")
            disable_db_runtime(exc)
    users = load_users()
    idx = find_user_index_by_billing_ids(users, customer_id, subscription_id)
    if idx is None:
        return None
    return users[idx]


def upsert_user(email, patch):
    email = (email or "").strip().lower()
    if not email:
        return None
    updates = patch or {}
    ensure_db_ready()
    if db_enabled():
        payload = {
            "email": email,
            "name": updates.get("name"),
            "picture": updates.get("picture"),
            "password_hash": updates.get("password_hash"),
            "provider": updates.get("provider"),
            "subscription_status": updates.get("subscription_status") or "free",
            "subscription_expires_at": updates.get("subscription_expires_at"),
            "subscription_updated_at": updates.get("subscription_updated_at"),
            "paddle_customer_id": updates.get("paddle_customer_id"),
            "paddle_subscription_id": updates.get("paddle_subscription_id"),
            "paddle_last_transaction_id": updates.get("paddle_last_transaction_id"),
            "paddle_last_event_type": updates.get("paddle_last_event_type"),
        }
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO users (
                            email,
                            name,
                            picture,
                            password_hash,
                            provider,
                            subscription_status,
                            subscription_expires_at,
                            subscription_updated_at,
                            paddle_customer_id,
                            paddle_subscription_id,
                            paddle_last_transaction_id,
                            paddle_last_event_type,
                            updated_at
                        )
                        VALUES (
                            %(email)s,
                            %(name)s,
                            %(picture)s,
                            %(password_hash)s,
                            %(provider)s,
                            %(subscription_status)s,
                            %(subscription_expires_at)s,
                            %(subscription_updated_at)s,
                            %(paddle_customer_id)s,
                            %(paddle_subscription_id)s,
                            %(paddle_last_transaction_id)s,
                            %(paddle_last_event_type)s,
                            NOW()
                        )
                        ON CONFLICT (email) DO UPDATE SET
                            name = COALESCE(EXCLUDED.name, users.name),
                            picture = COALESCE(EXCLUDED.picture, users.picture),
                            password_hash = COALESCE(EXCLUDED.password_hash, users.password_hash),
                            provider = COALESCE(EXCLUDED.provider, users.provider),
                            subscription_status = COALESCE(EXCLUDED.subscription_status, users.subscription_status),
                            subscription_expires_at = COALESCE(EXCLUDED.subscription_expires_at, users.subscription_expires_at),
                            subscription_updated_at = COALESCE(EXCLUDED.subscription_updated_at, users.subscription_updated_at),
                            paddle_customer_id = COALESCE(EXCLUDED.paddle_customer_id, users.paddle_customer_id),
                            paddle_subscription_id = COALESCE(EXCLUDED.paddle_subscription_id, users.paddle_subscription_id),
                            paddle_last_transaction_id = COALESCE(EXCLUDED.paddle_last_transaction_id, users.paddle_last_transaction_id),
                            paddle_last_event_type = COALESCE(EXCLUDED.paddle_last_event_type, users.paddle_last_event_type),
                            updated_at = NOW()
                        RETURNING *
                        """,
                        payload,
                    )
                    row = cur.fetchone()
                conn.commit()
            return row
        except Exception as exc:
            print(f"[db] upsert fallback for {email}: {exc}")
            disable_db_runtime(exc)
    users = load_users()
    idx = find_user_index(users, email)
    if idx is None:
        record = {
            "name": updates.get("name") or email,
            "email": email,
            "subscription_status": updates.get("subscription_status") or "free",
        }
        for key, value in updates.items():
            if value is not None:
                record[key] = value
        users.append(record)
        save_users(users)
        return record

    user = users[idx]
    changed = False
    for key, value in updates.items():
        if value is None:
            continue
        if user.get(key) != value:
            user[key] = value
            changed = True
    if changed:
        save_users(users)
    return user


def update_user_password(email, password_hash):
    email = (email or "").strip().lower()
    if not email or not password_hash:
        return None
    ensure_db_ready()
    if db_enabled():
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE users
                        SET password_hash = %s, updated_at = NOW()
                        WHERE lower(email) = %s
                        RETURNING *
                        """,
                        (password_hash, email),
                    )
                    row = cur.fetchone()
                conn.commit()
            return row
        except Exception as exc:
            print(f"[db] password update fallback for {email}: {exc}")
            disable_db_runtime(exc)
    users = load_users()
    updated_user = None
    for idx, u in enumerate(users):
        if u.get("email", "").lower() == email:
            users[idx]["password_hash"] = password_hash
            updated_user = users[idx]
            break
    if updated_user:
        save_users(users)
    return updated_user


def migrate_json_users_to_db():
    if not db_enabled():
        return
    try:
        if count_db_users() > 0:
            return
    except Exception as exc:
        print(f"[db] migration skipped; database unavailable during count: {exc}")
        return
    users = load_users()
    migrated = 0
    for user in users:
        email = (user.get("email") or "").strip().lower()
        if not email:
            continue
        try:
            upsert_user(email, user)
            migrated += 1
        except Exception as exc:
            print(f"[db] migration stopped; database unavailable during upsert: {exc}")
            break
    if migrated:
        print(f"[db] migrated {migrated} users from users.json to Postgres")


def parse_unix_timestamp(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_iso_timestamp(value):
    raw = str(value or "").strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(raw).timestamp()
    except ValueError:
        return None


def normalize_subscription_status(value):
    status = str(value or "free").strip().lower()
    if not status:
        return "free"
    return status


def is_premium_user(user_dict):
    status = normalize_subscription_status(user_dict.get("subscription_status"))
    if status not in PREMIUM_ACTIVE_STATUSES:
        return False
    expires_at = user_dict.get("subscription_expires_at")
    if not expires_at:
        return True
    expiry_ts = parse_unix_timestamp(expires_at)
    if expiry_ts is None:
        expiry_ts = parse_iso_timestamp(expires_at)
    if expiry_ts is None:
        return True
    return expiry_ts > time.time()


def session_user_payload(user_dict):
    name = user_dict.get("name") or user_dict.get("email")
    picture = user_dict.get("picture") or letter_avatar(name[:1] if name else "U")
    status = normalize_subscription_status(user_dict.get("subscription_status"))
    expires_at = user_dict.get("subscription_expires_at")
    payload = {
        "name": name,
        "email": user_dict.get("email"),
        "picture": picture,
        "subscription_status": status,
        "subscription_expires_at": expires_at,
    }
    payload["is_premium"] = is_premium_user(payload)
    return payload


def parse_paddle_signature(header_value):
    parts = {}
    for chunk in str(header_value or "").split(";"):
        if "=" not in chunk:
            continue
        key, value = chunk.split("=", 1)
        parts[key.strip()] = value.strip()
    return parts.get("ts"), parts.get("h1")


def verify_paddle_webhook_signature(raw_body, header_value, secret):
    timestamp, digest = parse_paddle_signature(header_value)
    if not timestamp or not digest or not secret:
        return False
    signed_payload = timestamp.encode("utf-8") + b":" + (raw_body or b"")
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, digest)


def extract_billing_identifiers(event_data):
    data = event_data if isinstance(event_data, dict) else {}
    custom_data = data.get("custom_data") if isinstance(data.get("custom_data"), dict) else {}
    customer = data.get("customer") if isinstance(data.get("customer"), dict) else {}
    billing_period = data.get("current_billing_period") if isinstance(data.get("current_billing_period"), dict) else {}
    scheduled_change = data.get("scheduled_change") if isinstance(data.get("scheduled_change"), dict) else {}
    email = (custom_data.get("user_email") or custom_data.get("email") or customer.get("email") or "").strip().lower()
    customer_id = (
        data.get("customer_id")
        or custom_data.get("customer_id")
        or customer.get("id")
        or ""
    )
    subscription_id = str(data.get("subscription_id") or "").strip()
    data_id = str(data.get("id") or "").strip()
    if not subscription_id and data_id.startswith("sub_"):
        subscription_id = data_id
    expires_at = (
        billing_period.get("ends_at")
        or data.get("next_billed_at")
        or scheduled_change.get("effective_at")
        or None
    )
    return {
        "email": email,
        "customer_id": str(customer_id or "").strip(),
        "subscription_id": subscription_id,
        "expires_at": expires_at,
    }


def resolve_subscription_status(event_type, event_data):
    normalized_type = str(event_type or "").strip().lower()
    raw_status = (event_data or {}).get("status")
    status_from_data = normalize_subscription_status(raw_status) if raw_status is not None else None
    if normalized_type == "transaction.completed":
        return "active"
    if normalized_type in {"transaction.payment_failed", "transaction.updated"} and status_from_data in {"past_due", "canceled"}:
        return status_from_data
    if normalized_type == "subscription.created":
        return "active"
    if normalized_type == "subscription.resumed":
        return "active"
    if normalized_type in {"subscription.canceled", "subscription.cancelled"}:
        return "canceled"
    if normalized_type == "subscription.paused":
        return "paused"
    if normalized_type == "subscription.past_due":
        return "past_due"
    if normalized_type == "subscription.trialing":
        return "trialing"
    if normalized_type == "subscription.updated":
        return status_from_data
    return status_from_data


def refresh_session_user_from_store():
    current = session.get("user")
    if not isinstance(current, dict):
        return
    email = (current.get("email") or "").strip().lower()
    if not email:
        normalized = session_user_payload(current)
        if normalized != current:
            session["user"] = normalized
        return
    persisted = find_user(email)
    base = dict(current)
    if persisted:
        base.update(
            {
                "name": persisted.get("name") or current.get("name"),
                "email": persisted.get("email") or email,
                "picture": current.get("picture") or persisted.get("picture"),
                "subscription_status": persisted.get("subscription_status", current.get("subscription_status")),
                "subscription_expires_at": persisted.get("subscription_expires_at", current.get("subscription_expires_at")),
            }
        )
    normalized = session_user_payload(base)
    if normalized != current:
        session["user"] = normalized

@app.route("/login-media/<path:filename>")
def login_media(filename):
    return send_from_directory(LOGIN_MEDIA_DIR, filename)

@app.route("/health")
def health():
    return jsonify({"ok": True}), 200


COUNTRY_INDICATOR_DEFS = {
    "gdpPerCapita": {"code": "NY.GDP.PCAP.CD"},
    "gniPerCapita": {"code": "NY.GNP.PCAP.CD"},
    "gdp": {"code": "NY.GDP.MKTP.CD"},
    "population": {"code": "SP.POP.TOTL"},
    "inflation": {"code": "FP.CPI.TOTL.ZG"},
    "unemployment": {"code": "SL.UEM.TOTL.ZS"},
}
COUNTRY_INDICATOR_CACHE = {}
COUNTRY_INDICATOR_CACHE_TTL = 6 * 60 * 60


def fetch_latest_country_indicator(country_code, indicator_code):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
    response = requests.get(url, params={"format": "json", "per_page": 8}, timeout=8)
    response.raise_for_status()
    payload = response.json()
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 and isinstance(payload[1], list) else []
    latest = next((row for row in rows if row.get("value") is not None), None)
    if not latest:
        return {"value": None, "year": ""}
    return {"value": latest.get("value"), "year": latest.get("date", "")}


@app.route("/api/country-indicators/<country_code>")
def country_indicators(country_code):
    code = re.sub(r"[^A-Za-z]", "", country_code or "").upper()[:3]
    if len(code) != 3:
        return jsonify({"error": "Invalid country code"}), 400

    now = time.time()
    cached = COUNTRY_INDICATOR_CACHE.get(code)
    if cached and now - cached["timestamp"] < COUNTRY_INDICATOR_CACHE_TTL:
        return jsonify(cached["data"])

    def load_metric(metric_key, indicator_code):
        try:
            return metric_key, fetch_latest_country_indicator(code, indicator_code)
        except requests.RequestException:
            return metric_key, {"value": None, "year": ""}

    metrics = {}
    with ThreadPoolExecutor(max_workers=len(COUNTRY_INDICATOR_DEFS)) as executor:
        futures = [
            executor.submit(load_metric, key, indicator["code"])
            for key, indicator in COUNTRY_INDICATOR_DEFS.items()
        ]
        for future in as_completed(futures):
            key, value = future.result()
            metrics[key] = value

    data = {"country_code": code, "metrics": metrics, "source": "World Bank"}
    COUNTRY_INDICATOR_CACHE[code] = {"timestamp": now, "data": data}
    return jsonify(data)


@app.route("/")
def index():
    user = session.get("user")
    cars, slug_map = load_cars()
    car_links = build_car_links(cars)
    featured_car_links = select_featured_car_links(car_links)
    featured_compare_links = build_featured_compare_links(cars, slug_map)
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "index.html",
        user=user,
        car_links=car_links,
        featured_car_links=featured_car_links,
        featured_compare_links=featured_compare_links,
        paddle_client_token=PADDLE_CLIENT_TOKEN,
        paddle_env=PADDLE_ENV,
        canonical_url=canonical_url,
        meta_title="CarQuantix - Smart Car Comparison",
        meta_description="Compare cars and motorcycles by horsepower, acceleration and top speed. Make smarter decisions with CarQuantix.",
        robots_directive="index,follow",
    )


@app.route("/news")
def news():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "news.html",
        news_items=NEWS_ITEMS,
        news_verified_on=NEWS_LAST_VERIFIED,
        canonical_url=canonical_url,
        meta_title="CarQuantix News - Verified Automotive Updates",
        meta_description="Verified automotive news, new model announcements, EV updates and auto show highlights curated from official sources.",
        robots_directive="index,follow",
    )


@app.route("/guides")
def guides():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "guides.html",
        guide_items=GUIDE_ITEMS,
        canonical_url=canonical_url,
        meta_title="CarQuantix Guides - Learn Cars Faster",
        meta_description="Beginner-friendly car guides about horsepower, comparisons, sports cars, EV choices and ownership cost.",
        robots_directive="index,follow",
    )


@app.route("/blog")
def blog():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "blog.html",
        blog_items=BLOG_ITEMS,
        canonical_url=canonical_url,
        meta_title="CarQuantix Blog - Car Writing and Editorials",
        meta_description="General car writing, editorial overviews and readable automotive topics from CarQuantix.",
        robots_directive="index,follow",
    )


@app.route("/privacy-policy")
def privacy_policy():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "privacy_policy.html",
        canonical_url=canonical_url,
        meta_title="CarQuantix Privacy Policy",
        meta_description="Read how CarQuantix collects, uses and protects your data.",
        robots_directive="index,follow",
    )


@app.route("/about-us")
def about_us():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "about_us.html",
        canonical_url=canonical_url,
        meta_title="About Us - CarQuantix",
        meta_description="Learn what CarQuantix does and how we help users compare vehicles with clear performance data.",
        robots_directive="index,follow",
    )


@app.route("/contact")
def contact():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "contact.html",
        canonical_url=canonical_url,
        meta_title="Contact - CarQuantix",
        meta_description="Contact the CarQuantix team for support, business or partnership requests.",
        robots_directive="index,follow",
    )

@app.route("/pricing")
def pricing():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "pricing.html",
        canonical_url=canonical_url,
        meta_title="Pricing - CarQuantix",
        meta_description="CarQuantix pricing and plan information.",
        robots_directive="index,follow",
    )


@app.route("/terms")
def terms():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "terms.html",
        canonical_url=canonical_url,
        meta_title="Terms and Conditions - CarQuantix",
        meta_description="Read the terms and conditions for using CarQuantix.",
        robots_directive="index,follow",
    )


@app.route("/refund-policy")
def refund_policy():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "refund_policy.html",
        canonical_url=canonical_url,
        meta_title="Refund Policy - CarQuantix",
        meta_description="Review the CarQuantix refund policy for subscriptions and digital services.",
        robots_directive="index,follow",
    )


@app.route("/api/billing/checkout", methods=["POST"])
def create_billing_checkout():
    user = session.get("user") or {}
    email = (user.get("email") or "").strip().lower()
    if not email:
        return jsonify({"ok": False, "message": "Login required."}), 401
    if not PADDLE_API_KEY or not PADDLE_PRICE_ID:
        return jsonify({"ok": False, "message": "Billing is not configured on the server."}), 500

    request_data = request.get_json(silent=True) or {}
    success_url = (request_data.get("success_url") or "").strip()
    if not success_url:
        success_url = f"{get_base_url()}/?billing=success"

    payload = {
        "items": [{"price_id": PADDLE_PRICE_ID, "quantity": 1}],
        "collection_mode": "automatic",
        "custom_data": {
            "user_email": email,
            "feature": "cost_of_ownership",
        },
        "checkout": {
            "success_url": success_url,
        },
        "customer": {"email": email},
    }
    headers = {
        "Authorization": f"Bearer {PADDLE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def extract_error_detail(body):
        detail = ""
        if isinstance(body, dict):
            if isinstance(body.get("error"), dict):
                detail = str(body["error"].get("detail") or body["error"].get("message") or "").strip()
            if not detail and isinstance(body.get("errors"), list) and body["errors"]:
                first_error = body["errors"][0] if isinstance(body["errors"][0], dict) else {}
                detail = str(first_error.get("detail") or first_error.get("message") or "").strip()
        return detail

    try:
        response = requests.post(
            f"{PADDLE_API_BASE}/transactions",
            headers=headers,
            json=payload,
            timeout=20,
        )
    except requests.RequestException as exc:
        return jsonify({"ok": False, "message": f"Checkout request failed: {exc}"}), 502

    try:
        body = response.json()
    except ValueError:
        body = {}

    if response.status_code >= 400:
        error_detail = extract_error_detail(body)
        message = "Failed to create checkout transaction."
        if error_detail:
            message = f"{message} {error_detail}"
        return jsonify({"ok": False, "message": message, "details": body}), 502

    transaction = body.get("data") if isinstance(body, dict) else {}
    checkout = transaction.get("checkout") if isinstance(transaction, dict) else {}
    checkout_url = checkout.get("url")
    if not checkout_url:
        return jsonify({"ok": False, "message": "Checkout URL was not returned by Paddle."}), 502

    transaction_id = transaction.get("id")
    update_patch = {}
    if transaction_id:
        update_patch["paddle_last_transaction_id"] = transaction_id
    tx_customer_id = str(transaction.get("customer_id") or "").strip()
    if tx_customer_id:
        update_patch["paddle_customer_id"] = tx_customer_id
    if update_patch:
        upsert_user(email, update_patch)
    return jsonify({"ok": True, "checkout_url": checkout_url, "transaction_id": transaction_id})


@app.route("/api/paddle/webhook", methods=["POST"])
def paddle_webhook():
    raw_body = request.get_data(cache=True, as_text=False) or b""
    if not verify_paddle_webhook_signature(
        raw_body,
        request.headers.get("Paddle-Signature", ""),
        PADDLE_WEBHOOK_SECRET,
    ):
        return jsonify({"ok": False, "message": "Invalid webhook signature."}), 400

    event = request.get_json(silent=True) or {}
    event_type = str(event.get("event_type") or "").strip().lower()
    event_data = event.get("data") if isinstance(event.get("data"), dict) else {}
    ids = extract_billing_identifiers(event_data)
    status = resolve_subscription_status(event_type, event_data)

    matched_user = find_user(ids["email"])
    if not matched_user:
        matched_user = find_user_by_billing_ids(ids["customer_id"], ids["subscription_id"])

    now_ts = int(time.time())
    patch = {
        "subscription_expires_at": ids["expires_at"],
        "subscription_updated_at": now_ts,
        "paddle_customer_id": ids["customer_id"] or None,
        "paddle_subscription_id": ids["subscription_id"] or None,
        "paddle_last_event_type": event_type or None,
    }
    if status is not None:
        patch["subscription_status"] = status
    if event_data.get("id") and str(event_data.get("id")).startswith("txn_"):
        patch["paddle_last_transaction_id"] = event_data.get("id")

    if not matched_user:
        if not ids["email"]:
            return jsonify({"ok": True, "message": "No matching user for webhook payload."}), 200
        new_user = {"name": ids["email"], "email": ids["email"], "subscription_status": "free"}
        for key, value in patch.items():
            if value is not None:
                new_user[key] = value
        upsert_user(ids["email"], new_user)
        return jsonify({"ok": True, "updated": ids["email"]}), 200

    updated_user = upsert_user(matched_user.get("email"), patch)
    return jsonify({"ok": True, "updated": (updated_user or matched_user).get("email")}), 200


@app.route("/api/billing/confirm", methods=["POST"])
def confirm_billing_transaction():
    user = session.get("user") or {}
    email = (user.get("email") or "").strip().lower()
    if not email:
        return jsonify({"ok": False, "message": "Login required."}), 401
    if not PADDLE_API_KEY:
        return jsonify({"ok": False, "message": "Billing is not configured on the server."}), 500

    request_data = request.get_json(silent=True) or {}
    transaction_id = str(request_data.get("transaction_id") or "").strip()
    if not transaction_id:
        return jsonify({"ok": False, "message": "Missing transaction id."}), 400

    headers = {
        "Authorization": f"Bearer {PADDLE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            f"{PADDLE_API_BASE}/transactions/{transaction_id}",
            headers=headers,
            timeout=20,
        )
    except requests.RequestException as exc:
        return jsonify({"ok": False, "message": f"Confirm request failed: {exc}"}), 502

    try:
        body = response.json()
    except ValueError:
        body = {}

    if response.status_code >= 400:
        return jsonify({"ok": False, "message": "Failed to fetch transaction.", "details": body}), 502

    data = body.get("data") if isinstance(body, dict) else {}
    if not isinstance(data, dict):
        data = {}

    custom_data = data.get("custom_data") if isinstance(data.get("custom_data"), dict) else {}
    customer = data.get("customer") if isinstance(data.get("customer"), dict) else {}
    data_email = (custom_data.get("user_email") or custom_data.get("email") or customer.get("email") or "").strip().lower()
    if data_email and data_email != email:
        return jsonify({"ok": False, "message": "Transaction does not match this user."}), 403

    status = normalize_subscription_status(data.get("status"))
    subscription_id = str(data.get("subscription_id") or "").strip()
    customer_id = str(data.get("customer_id") or "").strip()
    billing_period = data.get("current_billing_period") if isinstance(data.get("current_billing_period"), dict) else {}
    expires_at = billing_period.get("ends_at") or data.get("next_billed_at") or None

    completed_statuses = {"completed", "paid", "billed", "active"}
    if status not in completed_statuses and not subscription_id:
        return jsonify({"ok": False, "message": "Transaction not completed yet.", "status": status}), 200

    patch = {
        "subscription_status": "active",
        "subscription_updated_at": int(time.time()),
        "subscription_expires_at": expires_at,
        "paddle_customer_id": customer_id or None,
        "paddle_subscription_id": subscription_id or None,
        "paddle_last_transaction_id": transaction_id,
    }
    updated_user = upsert_user(email, patch)
    if updated_user:
        session["user"] = session_user_payload(updated_user)
    return jsonify({"ok": True, "status": "active"}), 200


@app.route("/cars/<slug>")
def car_detail(slug):
    _, slug_map = load_cars()
    car = slug_map.get(slug)
    if not car:
        year_swap = re.match(r"^(.+)-(\d{4})$", slug)
        if year_swap:
            alt_slug = f"{year_swap.group(2)}-{year_swap.group(1)}"
            car = slug_map.get(alt_slug)
            if car:
                canonical_slug = car.get("slug") or alt_slug
                return redirect(f"/cars/{canonical_slug}", code=301)
        return "Not Found", 404
    canonical_slug = car.get("slug") or slug
    if slug != canonical_slug:
        return redirect(f"/cars/{canonical_slug}", code=301)
    specs = build_car_specs(car)
    meta_title = f"{car.get('name', 'Car')} | CarQuantix"
    meta_description = build_car_meta_description(car)
    canonical_url = f"{get_base_url()}{request.path}"
    page_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": meta_title,
        "description": meta_description,
        "url": canonical_url,
    }
    return render_template(
        "car_detail.html",
        car=car,
        specs=specs,
        meta_title=meta_title,
        meta_description=meta_description,
        canonical_url=canonical_url,
        robots_directive="index,follow",
        page_schema=page_schema,
    )

@app.route("/car/<slug>")
def car_detail_legacy(slug):
    return redirect(f"/cars/{slug}", code=301)


@app.route("/compare/<compare_slug>")
def compare_detail(compare_slug):
    user = session.get("user")
    cars, slug_map = load_cars()
    resolved = resolve_compare_slug(compare_slug, slug_map)
    if not resolved:
        return "Not Found", 404
    if compare_slug != resolved["canonical_slug"]:
        return redirect(f"/compare/{resolved['canonical_slug']}", code=301)

    left_car = resolved["left_car"]
    right_car = resolved["right_car"]
    compare_rows = build_compare_spec_rows(left_car, right_car)
    compare_intro = build_compare_intro_content(left_car, right_car)
    compare_decision = build_compare_decision_data(left_car, right_car)
    race_video = build_compare_race_link(left_car, right_car)
    canonical_url = f"{get_base_url()}/compare/{resolved['canonical_slug']}"
    meta_title = f"{left_car.get('name')} vs {right_car.get('name')} | CarQuantix"
    meta_description = build_compare_meta_description(left_car, right_car)
    page_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": meta_title,
        "description": meta_description,
        "url": canonical_url,
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": left_car.get("name"), "url": f"{get_base_url()}/cars/{left_car.get('slug')}"},
                {"@type": "ListItem", "position": 2, "name": right_car.get("name"), "url": f"{get_base_url()}/cars/{right_car.get('slug')}"},
            ],
        },
    }
    return render_template(
        "compare_detail.html",
        user=user,
        left_car=left_car,
        right_car=right_car,
        compare_rows=compare_rows,
        compare_intro=compare_intro,
        compare_decision=compare_decision,
        race_video=race_video,
        comments_page=f"compare:{resolved['canonical_slug']}",
        canonical_url=canonical_url,
        meta_title=meta_title,
        meta_description=meta_description,
        robots_directive="index,follow",
        page_schema=page_schema,
    )


@app.route("/sitemap.xml")
def sitemap():
    cars, slug_map = load_cars()
    base_url = get_base_url()
    urls = [
        f"{base_url}/",
        f"{base_url}/news",
        f"{base_url}/guides",
        f"{base_url}/blog",
        f"{base_url}/about-us",
        f"{base_url}/contact",
        f"{base_url}/pricing",
        f"{base_url}/terms",
        f"{base_url}/refund-policy",
        f"{base_url}/privacy-policy",
    ]
    urls.extend(f"{base_url}/cars/{slug}" for slug in sorted(slug_map.keys()))
    urls.extend(f"{base_url}{entry['href']}" for entry in build_featured_compare_links(cars, slug_map))
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{entries}</urlset>"
    )
    return app.response_class(xml, mimetype="application/xml")

@app.route("/robots.txt")
def robots():
    base_url = CANONICAL_BASE_URL
    body = "User-agent: *\nAllow: /\n"
    body += f"Sitemap: {base_url}/sitemap.xml\n"
    return app.response_class(body, mimetype="text/plain")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(STATIC_DIR, "favicon.ico", mimetype="image/x-icon")

@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(ADS_TXT_DIR, "ads.txt", mimetype="text/plain")


@app.route("/<slug>")
def seo_slug(slug):
    normalized = re.sub(r"\s+", "-", (slug or "").strip().lower())
    if normalized in LEGACY_COMPARE_SLUGS:
        cars, slug_map = load_cars()
        left_ref, right_ref = LEGACY_COMPARE_SLUGS[normalized]
        left_car = resolve_car_reference(left_ref, cars, slug_map)
        right_car = resolve_car_reference(right_ref, cars, slug_map)
        if left_car and right_car:
            return redirect(build_compare_href(left_car, right_car), code=301)
        return "Not Found", 404
    if normalized in SEO_SLUGS:
        if normalized != slug:
            return redirect(f"/{normalized}", code=301)
        user = session.get("user")
        cars, slug_map = load_cars()
        car_links = build_car_links(cars)
        featured_car_links = select_featured_car_links(car_links)
        featured_compare_links = build_featured_compare_links(cars, slug_map)
        return render_template(
            "index.html",
            user=user,
            car_links=car_links,
            featured_car_links=featured_car_links,
            featured_compare_links=featured_compare_links,
            canonical_url=f"{get_base_url()}/",
            meta_title="CarQuantix - Compare Cars and Motorcycles",
            meta_description="Compare horsepower, acceleration and top speed with CarQuantix.",
            robots_directive="noindex,follow",
        )
    return "Not Found", 404

@app.route("/login/google")
def login_google():
    if 'google' not in oauth._registry:
        return jsonify({"ok": False, "message": "Google login not configured."}), 500
    print(f"[auth] using client_id={GOOGLE_CLIENT_ID}")
    redirect_uri = url_for("authorize_google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route("/auth/callback/google")
def authorize_google():
    if 'google' not in oauth._registry:
        return jsonify({"ok": False, "message": "Google login not configured."}), 500
    token = oauth.google.authorize_access_token()
    user = oauth.google.get("userinfo").json()
    email = (user.get("email") or "").strip().lower()
    if email:
        existing_user = find_user(email)
        persisted = upsert_user(
            email,
            {
                "name": user.get("name") or email,
                "picture": user.get("picture"),
                "provider": "google",
                "subscription_status": (existing_user or {}).get("subscription_status", "free"),
            },
        ) or user
        session["user"] = session_user_payload(persisted)
    else:
        session["user"] = session_user_payload(user)
    return redirect("/")

@app.route("/login/facebook")
def login_facebook():
    if 'facebook' not in oauth._registry:
        return jsonify({"ok": False, "message": "Facebook login not configured."}), 500
    redirect_uri = url_for("authorize_facebook", _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@app.route("/auth/callback/facebook")
def authorize_facebook():
    if 'facebook' not in oauth._registry:
        return jsonify({"ok": False, "message": "Facebook login not configured."}), 500
    token = oauth.facebook.authorize_access_token()
    # fetch name/email/picture
    user_info = oauth.facebook.get("me?fields=id,name,email,picture").json()
    picture = None
    try:
        picture = user_info.get("picture", {}).get("data", {}).get("url")
    except Exception:
        picture = None
    payload = {
        "name": user_info.get("name"),
        "email": user_info.get("email") or f"{user_info.get('id')}@facebook.com",
        "picture": picture,
        "provider": "facebook",
    }
    email = (payload.get("email") or "").strip().lower()
    existing_user = find_user(email)
    persisted = upsert_user(
        email,
        {
            "name": payload.get("name") or email,
            "picture": payload.get("picture"),
            "provider": "facebook",
            "subscription_status": (existing_user or {}).get("subscription_status", "free"),
        },
    ) if email else None
    session["user"] = session_user_payload(persisted or payload)
    return redirect("/")

@app.route("/auth/login", methods=["POST"])
def login_local():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify({"ok": False, "message": "Email and password are required."}), 400
    user = find_user(email)
    if not user or not verify_password(user.get("password_hash", ""), password):
        return jsonify({"ok": False, "message": "Invalid email or password."}), 401
    session["user"] = session_user_payload(user)
    return jsonify({"ok": True, "message": "Logged in."})


@app.route("/auth/signup", methods=["POST"])
def signup_local():
    # Deprecated direct signup path; keep for compatibility.
    return jsonify({"ok": False, "message": "Use /auth/signup/start and /auth/signup/verify."}), 400


@app.route("/auth/signup/start", methods=["POST"])
def signup_start():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "message": "Email and password are required."}), 400
    if find_user(email):
        return jsonify({"ok": False, "message": "An account with this email already exists."}), 400

    pending = prune_expired_pending()
    code = generate_verification_code()
    pending[email] = {
        "name": name or email,
        "email": email,
        "password_hash": generate_password_hash(password),
        "code": code,
        "expires_at": time.time() + PENDING_EXPIRY_SECONDS,
    }
    save_pending(pending)

    send_ok, send_msg = send_verification_email(email, code)
    print(f"[signup] verification code for {email}: {code}")
    resp = {
        "ok": True,
        "message": "Verification code sent to your email." if send_ok else "Verification code generated but email could not be sent.",
    }
    if app.debug or os.environ.get("EXPOSE_DEV_CODES") == "1" or not send_ok:
        resp["dev_code"] = code
    if not send_ok:
        resp["send_error"] = send_msg
    return jsonify(resp)


@app.route("/auth/signup/verify", methods=["POST"])
def signup_verify():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()
    if not email or not code:
        return jsonify({"ok": False, "message": "Email and code are required."}), 400

    pending = prune_expired_pending()
    entry = pending.get(email)
    if not entry:
        return jsonify({"ok": False, "message": "No verification pending for this email."}), 400
    if entry.get("code") != code:
        return jsonify({"ok": False, "message": "Invalid verification code."}), 400

    if find_user(email):
        pending.pop(email, None)
        save_pending(pending)
        return jsonify({"ok": False, "message": "Account already exists."}), 400

    user_record = {
        "name": entry.get("name") or email,
        "email": email,
        "password_hash": entry.get("password_hash"),
        "subscription_status": "free",
    }
    persisted_user = upsert_user(email, user_record) or user_record

    pending.pop(email, None)
    save_pending(pending)

    session["user"] = session_user_payload(persisted_user)
    return jsonify({"ok": True, "message": "Account created and verified."})


@app.route("/auth/forgot", methods=["POST"])
@app.route("/auth/forgot/start", methods=["POST"])
def forgot_password_start():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"ok": False, "message": "Email is required."}), 400

    user = find_user(email)
    if not user:
        # keep response generic to avoid leaking which emails exist
        return jsonify({"ok": True, "message": "If this email exists, a reset code has been sent."})

    pending = prune_expired_reset_pending()
    code = generate_verification_code()
    pending[email] = {
        "email": email,
        "code": code,
        "expires_at": time.time() + PENDING_EXPIRY_SECONDS,
    }
    save_reset_pending(pending)

    send_ok, send_msg = send_reset_email(email, code)
    print(f"[forgot] reset code for {email}: {code}")
    resp = {
        "ok": True,
        "message": "Reset code sent to your email." if send_ok else "Reset code generated but email could not be sent.",
    }
    if app.debug or os.environ.get("EXPOSE_DEV_CODES") == "1" or not send_ok:
        resp["dev_code"] = code
    if not send_ok:
        resp["send_error"] = send_msg
    return jsonify(resp)


@app.route("/auth/forgot/verify", methods=["POST"])
def forgot_password_verify():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()
    new_password = data.get("new_password") or ""

    if not email or not code or not new_password:
        return jsonify({"ok": False, "message": "Email, code, and new password are required."}), 400
    if len(new_password) < 8:
        return jsonify({"ok": False, "message": "Password must be at least 8 characters."}), 400

    pending = prune_expired_reset_pending()
    entry = pending.get(email)
    if not entry:
        return jsonify({"ok": False, "message": "No reset pending for this email."}), 400
    if entry.get("expires_at", 0) < time.time():
        pending.pop(email, None)
        save_reset_pending(pending)
        return jsonify({"ok": False, "message": "Reset code expired. Please request a new one."}), 400
    if entry.get("code") != code:
        return jsonify({"ok": False, "message": "Invalid reset code."}), 400

    updated_user = update_user_password(email, generate_password_hash(new_password))
    if not updated_user:
        pending.pop(email, None)
        save_reset_pending(pending)
        return jsonify({"ok": False, "message": "No account found for this email."}), 400

    pending.pop(email, None)
    save_reset_pending(pending)

    session["user"] = session_user_payload(updated_user)
    return jsonify({"ok": True, "message": "Password updated. You are now logged in."})


@app.route("/api/comments", methods=["GET"])
def get_comments():
    page = get_comment_page()
    comments = get_comments_for_page(page)
    return jsonify({"ok": True, "comments": comments})


@app.route("/api/comments", methods=["POST"])
def create_comment():
    identity = get_comment_identity()

    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "").strip()
    if len(text) < 10 or len(text) > 500:
        return jsonify({"ok": False, "message": "Comment must be between 10 and 500 characters."}), 400
    guest_username = str(data.get("username") or "").strip()
    if not identity and (len(guest_username) < 2 or len(guest_username) > 60):
        return jsonify({"ok": False, "message": "Name must be between 2 and 60 characters."}), 400

    try:
        rating = int(data.get("rating") or 5)
    except (TypeError, ValueError):
        rating = 5
    rating = max(1, min(5, rating))

    comment = _normalize_comment(
        {
            "id": _generate_comment_id("c"),
            "username": identity["username"] if identity else guest_username,
            "userId": identity["user_id"] if identity else None,
            "text": text,
            "page": get_comment_page(data.get("page")),
            "rating": rating,
            "date": datetime.utcnow().strftime("%d/%m/%Y"),
            "likes": [],
            "dislikes": [],
            "replies": [],
        }
    )

    comments = load_comments()
    comments.insert(0, comment)
    save_comments(comments)
    page_comments = get_comments_for_page(comment["page"], comments)
    return jsonify({"ok": True, "comment": comment, "comments": page_comments}), 201


@app.route("/api/comments/<comment_id>/like", methods=["POST"])
def toggle_comment_like(comment_id):
    identity = get_comment_identity()
    if not identity:
        return jsonify({"ok": False, "message": "Login required."}), 401

    comments = load_comments()
    target_comment = None
    for comment in comments:
        if comment.get("id") == comment_id:
            likes = [value for value in comment.get("likes", []) if value != identity["user_id"]]
            if len(likes) == len(comment.get("likes", [])):
                likes.append(identity["user_id"])
            comment["likes"] = likes
            target_comment = comment
            break

    if not target_comment:
        return jsonify({"ok": False, "message": "Comment not found."}), 404

    save_comments(comments)
    page = target_comment.get("page", "home")
    page_comments = get_comments_for_page(page, comments)
    return jsonify({"ok": True, "comment": target_comment, "comments": page_comments})


@app.route("/api/comments/<comment_id>/replies", methods=["POST"])
def create_comment_reply(comment_id):
    identity = get_comment_identity()
    if not identity:
        return jsonify({"ok": False, "message": "Login required."}), 401

    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "").strip()
    if len(text) < 1 or len(text) > 500:
        return jsonify({"ok": False, "message": "Reply must be between 1 and 500 characters."}), 400

    comments = load_comments()
    target_comment = None
    reply = _normalize_reply(
        {
            "id": _generate_comment_id("r"),
            "username": identity["username"],
            "userId": identity["user_id"],
            "text": text,
            "date": datetime.utcnow().strftime("%d/%m/%Y"),
        }
    )

    for comment in comments:
        if comment.get("id") == comment_id:
            replies = comment.get("replies", [])
            replies.insert(0, reply)
            comment["replies"] = replies
            target_comment = comment
            break

    if not target_comment:
        return jsonify({"ok": False, "message": "Comment not found."}), 404

    save_comments(comments)
    page = target_comment.get("page", "home")
    page_comments = get_comments_for_page(page, comments)
    return jsonify({"ok": True, "reply": reply, "comment": target_comment, "comments": page_comments}), 201


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    # Render (and most PaaS) provide the port via $PORT and require binding to 0.0.0.0
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
