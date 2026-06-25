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
from datetime import datetime, timedelta
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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
app.permanent_session_lifetime = timedelta(days=180)

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
CAR_LISTINGS_PATH = resolve_data_path("CAR_LISTINGS_PATH", "car_listings.json")
PENDING_EXPIRY_SECONDS = 600  # 10 minutes
LOGIN_MEDIA_DIR = Path(__file__).with_name("login logo")
STATIC_DIR = Path(__file__).with_name("static")
ADS_TXT_DIR = Path(__file__).with_name("ads.txt")
ICON_DIR = STATIC_DIR / "icon"
LISTING_UPLOAD_DIR = Path(
    os.environ.get(
        "LISTING_UPLOAD_DIR",
        str((Path(os.environ["APP_DATA_DIR"]).expanduser() / "listing-uploads") if os.environ.get("APP_DATA_DIR") else (STATIC_DIR / "listing-uploads")),
    )
).expanduser()
LISTING_IMAGE_LIMIT = 24
LISTING_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
LISTING_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
LISTING_FUEL_TYPES = {"Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in hybrid", "LPG"}
LISTING_CURRENCIES = [
    ("TRY", "TL", "Turkish Lira"),
    ("USD", "USD", "US Dollar"),
    ("EUR", "EUR", "Euro"),
    ("GBP", "GBP", "British Pound"),
    ("CHF", "CHF", "Swiss Franc"),
    ("CAD", "CAD", "Canadian Dollar"),
    ("AUD", "AUD", "Australian Dollar"),
    ("JPY", "JPY", "Japanese Yen"),
    ("CNY", "CNY", "Chinese Yuan"),
    ("AED", "AED", "UAE Dirham"),
    ("SAR", "SAR", "Saudi Riyal"),
    ("QAR", "QAR", "Qatari Riyal"),
    ("KWD", "KWD", "Kuwaiti Dinar"),
    ("NOK", "NOK", "Norwegian Krone"),
    ("SEK", "SEK", "Swedish Krona"),
    ("DKK", "DKK", "Danish Krone"),
    ("PLN", "PLN", "Polish Zloty"),
    ("CZK", "CZK", "Czech Koruna"),
    ("HUF", "HUF", "Hungarian Forint"),
    ("RON", "RON", "Romanian Leu"),
    ("BGN", "BGN", "Bulgarian Lev"),
    ("RUB", "RUB", "Russian Ruble"),
    ("UAH", "UAH", "Ukrainian Hryvnia"),
    ("GEL", "GEL", "Georgian Lari"),
    ("AZN", "AZN", "Azerbaijani Manat"),
    ("INR", "INR", "Indian Rupee"),
    ("KRW", "KRW", "South Korean Won"),
    ("SGD", "SGD", "Singapore Dollar"),
    ("HKD", "HKD", "Hong Kong Dollar"),
    ("BRL", "BRL", "Brazilian Real"),
    ("MXN", "MXN", "Mexican Peso"),
    ("ZAR", "ZAR", "South African Rand"),
]
LISTING_CURRENCY_BY_CODE = {code: {"code": code, "display": display, "name": name} for code, display, name in LISTING_CURRENCIES}
LISTING_CURRENCY_SYMBOLS = {
    "TRY": "₺",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "CHF": "CHF",
    "CAD": "C$",
    "AUD": "A$",
    "JPY": "¥",
    "CNY": "¥",
    "AED": "AED",
    "SAR": "SAR",
    "QAR": "QAR",
    "KWD": "KWD",
    "NOK": "NOK",
    "SEK": "SEK",
    "DKK": "DKK",
    "PLN": "PLN",
    "CZK": "CZK",
    "HUF": "HUF",
    "RON": "RON",
    "BGN": "BGN",
    "RUB": "₽",
    "UAH": "₴",
    "GEL": "₾",
    "AZN": "₼",
    "INR": "₹",
    "KRW": "₩",
    "SGD": "S$",
    "HKD": "HK$",
    "BRL": "R$",
    "MXN": "MX$",
    "ZAR": "ZAR",
}
LISTING_CURRENCY_ALIASES = {
    "TL": "TRY",
    "LIRA": "TRY",
    "TURKISH LIRA": "TRY",
    "DOLLAR": "USD",
    "DOLAR": "USD",
    "US DOLLAR": "USD",
    "EURO": "EUR",
    "POUND": "GBP",
    "STERLING": "GBP",
}
LISTING_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia",
    "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Democratic Republic of the Congo",
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany",
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan",
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
    "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
]
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
NEW_SEO_COMPARE_REFERENCES = [
    ("M5", "Panamera"),
    ("F8", "720S"),
    ("X5", "Q8"),
    ("NX", "GLC"),
    ("F-Type", "911"),
    ("Aventador", "LaFerrari"),
    ("Aventador", "SF90 Spider"),
    ("Revuelto", "Chiron"),
    ("Chiron", "LaFerrari"),
    ("SF90 Spider", "911 Turbo"),
    ("296", "Artura"),
    ("M4", "Camaro SS"),
    ("Mustang", "M4"),
    ("Supra", "GT-R"),
    ("R8", "SF90 Spider"),
]
FEATURED_COMPARE_REFERENCES = CURATED_COMPARE_REFERENCES + NEW_SEO_COMPARE_REFERENCES + [
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
FEATURED_COMPARE_LIMIT = int(os.environ.get("FEATURED_COMPARE_LIMIT", "30"))
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

# Only show comments that users actually submit. Synthetic review/comment seeds
# can make the site look misleading during AdSense review.
DEFAULT_COMMENTS = []
COMPARE_COMMENT_SEEDS = []

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

GUIDE_ARTICLE_SECTIONS = {
    "choose-a-sports-car": [
        {
            "heading": "Start with the job the car has to do",
            "paragraphs": [
                "A sports car that feels brilliant on a Sunday morning can become the wrong choice if it has to handle school runs, winter roads, heavy traffic, or long motorway days. Before looking at horsepower, write down the real use case: weekend drives, daily commuting, track days, or a mixed role. That first filter removes cars that only look right on a spec sheet.",
                "The best short list usually includes cars with similar price, age, body style, and running cost. Comparing a lightweight two-seat coupe with a heavy luxury GT can be fun, but it rarely answers a buying question unless you are honest about comfort, luggage space, fuel use, tire cost, and servicing.",
            ],
            "bullets": [
                "Weekend use can prioritize steering feel, sound, and weight.",
                "Daily use should add visibility, ride comfort, and cabin ergonomics.",
                "Track use needs brakes, tire availability, cooling, and reliability history.",
            ],
        },
        {
            "heading": "Use power as one input, not the whole decision",
            "paragraphs": [
                "Horsepower matters, but it does not explain how easy a car is to drive quickly. Weight, gearing, traction, tire compound, and suspension setup can make a lower-power car feel sharper and more confidence-inspiring than a heavier model with a bigger number. That is why CarQuantix shows acceleration, top speed, engine type, and price together instead of isolating one headline metric.",
                "For road driving, repeatable acceleration and usable torque often matter more than a maximum power figure reached near the top of the rev range. A car with less peak power but better traction can feel faster in normal conditions, especially in wet weather or on uneven roads.",
            ],
        },
        {
            "heading": "Look beyond the purchase price",
            "paragraphs": [
                "Sports cars often hide cost in tires, brakes, insurance, depreciation, and scheduled maintenance. Large wheels and high-performance tires can make routine ownership noticeably more expensive. Carbon-ceramic brakes, exotic tire sizes, or rare body panels can also change the financial picture even when the initial price looks attractive.",
                "A practical buying comparison should estimate one full year of ownership. Include expected mileage, fuel or charging cost, insurance, service intervals, tire replacement, tax, and likely resale value. This turns the question from which car is fastest into which car fits your budget without constant compromise.",
            ],
        },
        {
            "heading": "Build a balanced short list",
            "paragraphs": [
                "A strong short list normally has one emotional choice, one value choice, and one safe choice. The emotional choice is the car you want most. The value choice offers the best performance or usability for the money. The safe choice is the one with the clearest ownership case. If one model wins two of those roles, it deserves serious attention.",
                "Use the comparison table to check the obvious numbers, then read owner reports and professional reviews for ride quality, reliability, and day-to-day usability. Specs start the decision; real-world ownership context finishes it.",
            ],
        },
    ],
    "what-is-horsepower": [
        {
            "heading": "What horsepower actually measures",
            "paragraphs": [
                "Horsepower is a measure of how quickly an engine or motor can do work. In simple terms, it describes the rate at which energy is delivered. More horsepower can support stronger acceleration and a higher top speed, but only if the rest of the vehicle can turn that output into motion effectively.",
                "Two cars with the same horsepower can feel completely different. One may deliver power smoothly across the rev range, while another may only feel strong at high rpm. Electric vehicles can deliver torque instantly, while turbocharged combustion engines may build boost before peak output arrives.",
            ],
        },
        {
            "heading": "Horsepower versus torque",
            "paragraphs": [
                "Torque describes twisting force, while horsepower combines torque with engine speed. Torque strongly affects the feeling of pull at low and mid speeds. Horsepower becomes more important as speed rises and the car needs sustained power to keep accelerating against aerodynamic drag.",
                "A high-torque car can feel effortless in traffic and when overtaking. A high-horsepower car can feel more dramatic as speed builds. Neither number should be read alone, because gearing and vehicle weight decide how those numbers reach the road.",
            ],
        },
        {
            "heading": "Why weight changes the answer",
            "paragraphs": [
                "Power-to-weight ratio is often more useful than horsepower alone. A lighter car needs less energy to accelerate, brake, and change direction. This is why lightweight sports cars can feel lively even when their horsepower is modest next to modern performance sedans or SUVs.",
                "Weight also affects tire wear, brake temperatures, and agility. If two cars have similar power, the lighter one may feel more responsive. If a heavier car has much more power, it may win straight-line acceleration but still feel less precise on a twisty road.",
            ],
        },
        {
            "heading": "How to use horsepower in CarQuantix",
            "paragraphs": [
                "Use horsepower as a starting point, then compare 0-100 km/h, top speed, engine type, fuel or energy consumption, and price. When those numbers tell the same story, the performance ranking is straightforward. When they conflict, the better car depends on your priorities.",
                "For a buying decision, ask what the number means in daily use: will the car be easier to overtake with, more expensive to fuel, harder to insure, or simply more enjoyable? The useful answer is not the biggest number; it is the number that fits the job.",
            ],
        },
    ],
    "how-to-compare-cars": [
        {
            "heading": "Compare cars inside the same real category",
            "paragraphs": [
                "The first rule of useful comparison is matching cars that solve the same problem. Body style, price range, model year, and intended use matter. A luxury SUV and a lightweight coupe can both be quick, but they serve different drivers and should not be judged by acceleration alone.",
                "Start by asking whether both cars would realistically appear on the same shopping list. If the answer is no, the comparison can still be interesting, but it should be read as entertainment or research rather than a direct buying decision.",
            ],
        },
        {
            "heading": "Use a group of metrics",
            "paragraphs": [
                "A good comparison uses several metrics at once: horsepower, 0-100 km/h, top speed, engine type, consumption, and price. Each metric explains a different part of the ownership experience. Acceleration shows launch and traction. Top speed shows high-speed capability. Consumption and price reveal day-to-day cost pressure.",
                "CarQuantix places these values in one table so the trade-offs are visible. A car can be faster but more expensive, cheaper but slower, or more efficient but less emotional. The table helps identify where the compromise actually sits.",
            ],
            "bullets": [
                "Use 0-100 km/h for short acceleration comparisons.",
                "Use top speed for high-speed capability, not daily usefulness.",
                "Use consumption and price to test the ownership case.",
            ],
        },
        {
            "heading": "Separate objective data from preference",
            "paragraphs": [
                "Specs can show which car is quicker or cheaper, but they cannot fully measure design, sound, steering feel, comfort, or brand preference. Those subjective factors are still valid. The mistake is pretending they are data. Treat the table as the objective layer and your preferences as the personal layer.",
                "This approach makes decisions clearer. If one car wins on numbers and the other wins emotionally, you can decide knowingly instead of forcing the data to support the choice you already wanted.",
            ],
        },
        {
            "heading": "Check the source and freshness of data",
            "paragraphs": [
                "Vehicle data can vary by market, trim, transmission, tire package, battery size, and model year. Use published figures as a comparison baseline, not a promise that every local version is identical. When a detail matters, confirm the exact trim from the manufacturer or seller before buying.",
                "CarQuantix is designed for fast research and shortlist building. It should help you find the right questions to ask next: Which trim is this? Which market figure is being used? What does ownership cost after fuel, tires, insurance, and depreciation?",
            ],
        },
    ],
    "understanding-0-100": [
        {
            "heading": "What a 0-100 km/h time tells you",
            "paragraphs": [
                "A 0-100 km/h figure shows how quickly a car accelerates from a standstill to road speed under test conditions. It is useful because it compresses launch traction, engine response, gearing, weight, and tire performance into one easy number.",
                "The number is not a complete performance score. It says little about braking, cornering, high-speed stability, comfort, or repeatability. A car can have a strong 0-100 time and still feel less satisfying than a slower car on real roads.",
            ],
        },
        {
            "heading": "Why launch conditions matter",
            "paragraphs": [
                "Factory acceleration numbers are often recorded with ideal surfaces, fresh tires, experienced drivers, and launch control where available. All-wheel drive cars can gain a major advantage from a standing start because they distribute torque more effectively.",
                "On a normal road, temperature, tire age, surface quality, driver reaction, and fuel or battery state can change the result. That is why a small difference on paper is not always meaningful in daily driving.",
            ],
        },
        {
            "heading": "How to read close results",
            "paragraphs": [
                "If two cars are separated by a tenth or two, treat them as effectively similar unless repeat tests show a consistent gap. A half-second difference is easier to feel. A difference of one second or more usually changes the character of the car noticeably.",
                "For buying, ask whether the acceleration advantage supports your actual use. A quicker launch may matter for track days or enthusiast driving, while ride quality, fuel use, or cabin space may matter more for a daily commute.",
            ],
        },
        {
            "heading": "Use acceleration with other metrics",
            "paragraphs": [
                "Acceleration is most useful when compared with horsepower, weight, transmission type, and price. A car with moderate power but a strong 0-100 time may have excellent traction and gearing. A car with high power but a slower time may struggle with weight or grip.",
                "CarQuantix shows 0-100 km/h beside other specs so the number has context. This helps separate genuine performance from a single impressive statistic.",
            ],
        },
    ],
    "fuel-vs-hybrid-vs-ev": [
        {
            "heading": "Match the powertrain to your routine",
            "paragraphs": [
                "The best powertrain depends on where and how you drive. A gasoline car can still make sense for irregular long trips, rural use, or drivers without predictable charging. A hybrid can reduce fuel use in traffic without requiring a charging habit. An EV can be excellent when home or workplace charging is easy.",
                "Before comparing performance, map your weekly driving. Annual mileage, trip length, parking situation, climate, electricity price, and charging access all affect the ownership result.",
            ],
        },
        {
            "heading": "When gasoline still works",
            "paragraphs": [
                "Combustion cars remain convenient for drivers who take frequent long trips, need quick refueling, or live where charging infrastructure is weak. They may also be lighter than comparable EVs, which can help steering feel and tire wear in some performance cars.",
                "The trade-off is running cost and emissions. Fuel prices, maintenance, and city traffic can make a traditional powertrain more expensive over time, especially for high-mileage drivers.",
            ],
        },
        {
            "heading": "Where hybrids fit",
            "paragraphs": [
                "Hybrids are useful when you want lower fuel consumption without fully changing your routine. They work especially well in stop-start traffic because the electric motor can reduce engine load and recover energy through braking.",
                "A hybrid is not automatically the cheapest option. Purchase price, battery warranty, service requirements, and highway efficiency all matter. Compare the full ownership cost instead of assuming the badge guarantees savings.",
            ],
        },
        {
            "heading": "When an EV is strongest",
            "paragraphs": [
                "An EV is strongest when charging is predictable and cheap. Home charging can make day-to-day use very convenient, and instant torque can make even ordinary EVs feel quick in city driving. Lower mechanical complexity can also reduce some routine maintenance needs.",
                "The weaknesses are charging time, cold-weather range loss, highway energy use, and public charger reliability. If those are manageable in your routine, an EV can be the most practical and efficient choice.",
            ],
        },
    ],
    "ownership-cost": [
        {
            "heading": "Think in annual cost, not purchase price",
            "paragraphs": [
                "Ownership cost is the amount a vehicle costs to run over time, not just the price you pay on day one. Fuel or charging, insurance, tax, maintenance, tires, financing, depreciation, and repairs all belong in the calculation.",
                "A cheaper car can become expensive if it has high fuel use, costly tires, poor resale value, or frequent service needs. A more expensive car can sometimes be easier to justify if it holds value and has predictable running costs.",
            ],
        },
        {
            "heading": "Fuel and energy are only one line",
            "paragraphs": [
                "Fuel cost is easy to calculate, so it often gets too much attention. It matters, especially for high-mileage drivers, but depreciation and insurance can outweigh fuel savings. Performance cars can also add large tire and brake costs that are not obvious from the spec sheet.",
                "Use the fuel calculator for a quick estimate, then add the hidden items manually. The more expensive the car, the more important depreciation becomes.",
            ],
        },
        {
            "heading": "Performance parts change the budget",
            "paragraphs": [
                "Large wheels, wide tires, adaptive dampers, carbon-ceramic brakes, complex hybrid systems, and rare body panels can all raise ownership cost. These features may be worth it, but they should be counted before buying.",
                "A practical comparison includes realistic tire replacement, brake service, and warranty coverage. If the car will be driven hard, add more margin for consumables.",
            ],
        },
        {
            "heading": "Build a simple ownership worksheet",
            "paragraphs": [
                "Create a yearly estimate with expected distance, fuel or electricity price, insurance, service, tires, tax, financing, and depreciation. Then compare that number between vehicles. This gives a clearer answer than looking at monthly payment alone.",
                "CarQuantix helps with the first layer by placing consumption and performance data together. The final step is adapting those figures to your local prices and your real mileage.",
            ],
        },
    ],
}
COMPARE_SEO_OVERRIDES = {
    "2018-porsche-panamera-vs-2024-bmw-m5": {
        "title": "BMW M5 vs Porsche Panamera: Performance, Price, Reliability and Daily Driving",
        "meta_description": "Compare the BMW M5 and Porsche Panamera by performance, price, reliability, comfort, maintenance cost and daily driving to decide which one fits you better.",
        "quick_verdict": "The BMW M5 is better if you want stronger performance, a sportier driving feel and more direct pace, while the Porsche Panamera makes more sense if luxury comfort and grand-touring polish matter more.",
        "reverse_keyword": "Porsche Panamera vs BMW M5",
        "related_compare_links": [
            ("BMW M5 vs Audi RS7", "M5", "RS7"),
            ("BMW M5 vs Mercedes E63 AMG", "M5", "E 63 AMG"),
            ("Porsche Panamera vs Audi RS7", "Panamera", "RS7"),
        ],
        "extra_links": [
            {"href": "/blog/super-sedan-vs-coupe", "title": "Best Luxury Performance Sedans"},
        ],
    },
    "2018-mclaren-720s-vs-2023-ferrari-f8": {
        "title": "Ferrari F8 vs McLaren 720S: Speed, Price, Reliability and Driving Experience",
        "meta_description": "Compare the Ferrari F8 and McLaren 720S by speed, price, reliability, maintenance cost and driving experience before choosing the better supercar.",
        "quick_verdict": "The McLaren 720S is the sharper pick for outright speed and acceleration, while the Ferrari F8 is better if brand character, engine drama and emotional appeal matter most.",
    },
    "2024-audi-q8-vs-2024-bmw-x5": {
        "title": "BMW X5 vs Audi Q8: Luxury SUV Comparison, Price, Comfort and Reliability",
        "meta_description": "Compare the BMW X5 and Audi Q8 by price, comfort, reliability, performance, maintenance cost and daily driving to choose the better luxury SUV.",
        "quick_verdict": "The BMW X5 is the better all-round luxury SUV for balanced performance and practicality, while the Audi Q8 is the stronger choice if design, cabin style and relaxed cruising are your priorities.",
        "reverse_keyword": "Audi Q8 vs BMW X5",
        "related_compare_links": [
            ("BMW X5 vs Mercedes GLE", "X5", "GLE"),
            ("Audi Q8 vs Mercedes GLE", "Q8", "GLE"),
            ("Lexus LX vs BMW X5", "LX", "X5"),
        ],
        "extra_links": [
            {"href": "/blog/super-sedan-vs-coupe", "title": "Best Luxury SUVs"},
        ],
    },
    "2024-lexus-nx-vs-2024-mercedes-benz-glc": {
        "title": "Lexus NX vs Mercedes GLC: Reliability, Comfort, Price and Daily Driving",
        "meta_description": "Compare the Lexus NX and Mercedes GLC by reliability, comfort, price, maintenance cost, performance and daily driving to choose the better luxury SUV.",
        "quick_verdict": "The Lexus NX is better if reliability, running costs and ownership peace of mind are your priorities, while the Mercedes GLC is stronger if cabin prestige and refinement matter more.",
    },
    "2022-porsche-911-vs-2024-jaguar-f-type": {
        "title": "Jaguar F-Type vs Porsche 911: Sports Car Comparison, Price and Driving Feel",
        "meta_description": "Compare the Jaguar F-Type and Porsche 911 by performance, price, reliability, maintenance cost and driving feel before choosing the better sports car.",
        "quick_verdict": "The Porsche 911 is the stronger all-round sports car for performance, precision and resale strength, while the Jaguar F-Type is best for buyers who want style, sound and grand-touring character.",
    },
}

BLOG_ARTICLE_SECTIONS = {
    "fastest-cars-in-2026": [
        {
            "heading": "Speed is no longer just a top-speed number",
            "paragraphs": [
                "The fastest cars people discuss in 2026 are not judged by top speed alone. Acceleration, repeatability, hybrid assistance, electric torque delivery, aerodynamics, tire technology, and brand story all shape the conversation. A car that can launch hard again and again may feel more relevant than a machine built only for one extreme run.",
                "That is why modern performance debates often compare different kinds of speed. Hypercars chase very high ceilings, electric sedans deliver instant response, and lightweight sports cars focus on feel. Each offers a different answer to the same question: what does fast actually mean to the driver?",
            ],
        },
        {
            "heading": "Acceleration changed the public benchmark",
            "paragraphs": [
                "A decade ago, top speed carried more weight in casual car conversations. Today, 0-100 km/h and quarter-mile performance are easier to understand and easier to experience. Electric vehicles pushed that shift because instant torque made extreme launch figures more common.",
                "The result is a broader performance field. A family EV can now post acceleration numbers that once belonged to supercars, while dedicated sports cars must prove their value through handling, braking, consistency, sound, and engagement.",
            ],
        },
        {
            "heading": "Top speed still matters, but context matters more",
            "paragraphs": [
                "Top speed remains technically impressive because it requires power, aero stability, cooling, tire capability, and gearing. It is also the least accessible metric for normal drivers. Few owners will ever use a maximum speed figure, which makes the number more symbolic than practical.",
                "For research, top speed is best read alongside acceleration and power. A very high top speed suggests strong engineering depth, but it does not automatically make a car more enjoyable or more useful on ordinary roads.",
            ],
        },
        {
            "heading": "The useful way to compare fast cars",
            "paragraphs": [
                "Use CarQuantix to compare the numbers, then separate the cars by purpose. A luxury GT, a track-focused coupe, a hypercar, and a performance EV can all be fast, but they are fast in different ways. The strongest comparison asks which type of speed fits the use case.",
                "The cars that remain interesting are usually the ones with a clear identity. Raw performance gets attention, but balance keeps a car in the conversation.",
            ],
        },
    ],
    "best-sports-cars-under-50k": [
        {
            "heading": "The under-50k segment is about trade-offs",
            "paragraphs": [
                "Sports cars under 50k rarely win by being perfect. They win by giving buyers a strong mix of feel, reliability, running cost, performance, and everyday usability. The right choice depends less on a universal ranking and more on what compromise you accept.",
                "Some cars focus on lightness and steering. Others offer more power, better comfort, or easier daily use. A smart buyer decides which experience matters before comparing the numbers.",
            ],
        },
        {
            "heading": "Power is tempting, but weight is decisive",
            "paragraphs": [
                "In this price range, a lighter car with modest power can feel more alive than a heavier car with a bigger engine. Lower weight helps braking, steering, tire wear, and fuel use. It can also make legal road speeds more engaging.",
                "A high-power option may still be the right answer if straight-line speed and tuning potential matter most. The important step is knowing whether you value lap-time potential, road feel, comfort, or easy ownership.",
            ],
        },
        {
            "heading": "Daily usability should not be ignored",
            "paragraphs": [
                "A car that is difficult to see out of, harsh over broken roads, or expensive to insure can lose its appeal quickly. Seat comfort, cabin noise, cargo room, technology, and service access all matter if the car is more than a weekend toy.",
                "Buyers should also check tire sizes, fuel economy, and common service items. These practical details can separate a fun purchase from a car that becomes stressful to keep.",
            ],
        },
        {
            "heading": "How to build a better short list",
            "paragraphs": [
                "Choose three finalists: the most emotional option, the most practical option, and the best value option. Compare horsepower, acceleration, top speed, price, and consumption, then add local ownership costs. This turns a broad market into a manageable decision.",
                "The best under-50k sports car is the one you can enjoy often, maintain properly, and still feel excited to drive after the first month.",
            ],
        },
    ],
    "why-evs-are-growing": [
        {
            "heading": "EV growth is driven by convenience as much as efficiency",
            "paragraphs": [
                "Electric cars are becoming more popular because they can make everyday driving simpler for people with reliable charging. Waking up to a charged vehicle changes the ownership routine. Instant torque, quiet operation, and lower local emissions add to the appeal.",
                "The shift is not only about environmental messaging. For many drivers, the strongest argument is practical: fewer fuel stops, strong city performance, and smoother low-speed driving.",
            ],
        },
        {
            "heading": "Software changed buyer expectations",
            "paragraphs": [
                "Modern EVs often feel like software products as much as vehicles. Navigation, charging route planning, remote climate control, over-the-air updates, and energy monitoring are part of the ownership experience. Buyers now compare digital convenience alongside acceleration and range.",
                "This software layer can be a strength or a weakness. A good interface makes the car easier to live with. A confusing or unreliable interface can damage trust even when the hardware is strong.",
            ],
        },
        {
            "heading": "Charging access decides the experience",
            "paragraphs": [
                "The same EV can be excellent for one owner and frustrating for another. Home charging, workplace charging, public charger density, weather, electricity prices, and trip length all change the answer. That is why EV advice should start with the driver's routine.",
                "For buyers without dependable charging, a hybrid or efficient combustion car may still be more practical. The right comparison is not EV versus gasoline in general; it is EV versus gasoline for a specific driver.",
            ],
        },
        {
            "heading": "What to compare before choosing an EV",
            "paragraphs": [
                "Look at usable range, charging speed, efficiency, battery warranty, cabin packaging, weight, and tire cost. Acceleration is often strong, but ownership value depends on more than a quick launch.",
                "CarQuantix helps by showing performance and consumption together. The next step is applying local charging prices and real route needs to the numbers.",
            ],
        },
    ],
    "super-sedan-vs-coupe": [
        {
            "heading": "The two body styles solve different problems",
            "paragraphs": [
                "A super sedan tries to combine speed with space, comfort, and everyday usability. A coupe usually gives up some practicality for style, lower seating, and a more focused driving feel. Both can be fast, but they create different ownership experiences.",
                "The right choice depends on whether the car needs to carry passengers and luggage regularly. If it does, the sedan's flexibility can make it easier to enjoy more often.",
            ],
        },
        {
            "heading": "Performance numbers do not tell the whole story",
            "paragraphs": [
                "Modern super sedans can be extremely quick because they often use powerful engines, all-wheel drive, and advanced launch systems. Coupes may be lighter or more emotional, but not always faster in a straight line.",
                "Handling feel can also differ. A coupe may feel more special from the driver's seat, while a sedan may offer more stability and confidence in poor weather. The spec table starts the comparison, but the driving environment finishes it.",
            ],
        },
        {
            "heading": "Ownership cost and depreciation matter",
            "paragraphs": [
                "Large performance sedans can bring expensive tires, brakes, suspension parts, and insurance. Coupes can be expensive too, especially if they use rare parts or exotic construction. Depreciation varies widely by brand, engine, and desirability.",
                "A buyer should compare not only purchase price but also yearly running cost. The more powerful and heavier the car, the more attention tires and brakes deserve.",
            ],
        },
        {
            "heading": "Which one makes more sense",
            "paragraphs": [
                "A super sedan makes more sense when one car must do everything. A coupe makes more sense when the purchase is mainly about emotion, design, or focused driving. Neither answer is automatically better.",
                "Use CarQuantix to compare speed, power, and cost data, then decide how much practicality you are willing to trade for character.",
            ],
        },
    ],
    "digital-cockpit-trend": [
        {
            "heading": "Dashboards became software surfaces",
            "paragraphs": [
                "Modern dashboards feel more digital because many vehicle functions are now controlled through software. Navigation, media, climate, driver assistance, charging, drive modes, and vehicle settings often live on central displays or digital clusters.",
                "This gives manufacturers flexibility. They can update interfaces, add features, and simplify physical production. The downside is that basic tasks can become harder if the interface is poorly organized.",
            ],
        },
        {
            "heading": "Good digital design reduces friction",
            "paragraphs": [
                "A good cockpit puts frequent actions where drivers expect them. Climate controls, drive mode selection, defogging, volume, and navigation should be quick to reach. Visual design should support driving, not compete for attention.",
                "Large screens are not automatically better. The useful question is whether the system helps the driver act quickly and confidently while moving.",
            ],
        },
        {
            "heading": "Physical controls still have value",
            "paragraphs": [
                "Buttons, knobs, and stalks can be easier to use without looking away from the road. Many buyers still prefer physical controls for core functions because muscle memory matters. A balanced cockpit uses digital screens where they add value and physical controls where speed matters.",
                "The strongest interiors usually avoid turning every simple task into a menu. They use software for rich information and hardware for repeated actions.",
            ],
        },
        {
            "heading": "What buyers should check",
            "paragraphs": [
                "Before buying, test the interface while parked and during a short drive. Try climate changes, navigation entry, audio controls, drive modes, and phone pairing. If the basic tasks feel annoying on day one, they may feel worse after months of ownership.",
                "Interior technology should make the car easier to live with. It should not be a spec-sheet feature that adds distraction.",
            ],
        },
    ],
    "why-weight-matters": [
        {
            "heading": "Weight affects every part of performance",
            "paragraphs": [
                "Weight matters because a vehicle must accelerate, brake, turn, and support that mass every time it moves. More horsepower can hide weight in a straight line, but it cannot erase the effect on tires, brakes, suspension, and agility.",
                "A lighter car often feels more responsive because it needs less force to change direction. That feeling can be more important to enjoyment than a larger power number.",
            ],
        },
        {
            "heading": "Power-to-weight is more useful than power alone",
            "paragraphs": [
                "Power-to-weight ratio explains how much output each unit of mass has to move. Two cars with similar horsepower can perform differently if one is much heavier. A lower-power lightweight car can stay competitive against a heavier car with a stronger engine.",
                "This is why pure horsepower comparisons can mislead buyers. The better question is how effectively the vehicle uses its power.",
            ],
        },
        {
            "heading": "Heavy cars spend more on consumables",
            "paragraphs": [
                "Weight increases the load on tires and brakes. Heavy performance vehicles can be very fast, but they may also use expensive tires more quickly and put more heat into the braking system. This affects both running cost and repeatable performance.",
                "For EVs and large SUVs, battery and structure weight can make this especially important. Strong acceleration does not always mean low ownership cost.",
            ],
        },
        {
            "heading": "How to use weight in a buying decision",
            "paragraphs": [
                "When comparing cars, read weight together with horsepower, acceleration, tire size, brake equipment, and intended use. A heavy car may be perfect for comfort and stability. A light car may be better for feedback and lower consumable cost.",
                "The right answer depends on what you value. Weight is not always bad, but ignoring it makes performance comparisons incomplete.",
            ],
        },
    ],
}


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
    car_data = car or {}
    name = str(car_data.get("name") or "this car").strip()
    bits = []
    if car_data.get("power") is not None:
        bits.append(f"{car_data['power']} hp")
    if car_data.get("acc") is not None:
        bits.append(f"0-100 km/h in {car_data['acc']} s")
    if car_data.get("topSpeed") is not None:
        bits.append(f"{car_data['topSpeed']} km/h top speed")

    if bits:
        stats = ", ".join(bits[:3])
        description = (
            f"Explore the {name} with {stats}, engine details, price insights "
            "and comparisons against similar performance cars."
        )
        if len(description) <= 160:
            return description
        return (
            f"Explore the {name}: {stats}, engine details and similar "
            "performance car comparisons."
        )

    return (
        f"Explore the {name} with engine details, performance specs, price insights "
        "and comparisons against similar cars on CarQuantix."
    )


def format_consumption_text(car):
    consumption = (car or {}).get("consumption") or {}
    value = consumption.get("value")
    unit = consumption.get("unit")
    if value is None or not unit:
        return ""
    return f"{value} {unit}"


def build_car_detail_content(car):
    name = str((car or {}).get("name") or "This model").strip()
    engine = str((car or {}).get("engine") or "").strip()
    price = format_display_price((car or {}).get("price"))
    consumption_text = format_consumption_text(car)
    power = (car or {}).get("power")
    acceleration = (car or {}).get("acc")
    top_speed = (car or {}).get("topSpeed")

    performance_bits = []
    if power is not None:
        performance_bits.append(f"{power} hp")
    if acceleration is not None:
        performance_bits.append(f"0-100 km/h in {acceleration} seconds")
    if top_speed is not None:
        performance_bits.append(f"a {top_speed} km/h top speed")

    if performance_bits:
        summary = f"{name} is listed with {', '.join(performance_bits)}."
    else:
        summary = f"{name} is listed as part of the CarQuantix vehicle database."

    if engine:
        summary += f" The recorded powertrain is {engine}."
    if price != "-":
        summary += f" The listed price is {price}, so it should be read beside the performance figures rather than as a separate detail."
    if consumption_text:
        summary += f" Recorded consumption is {consumption_text}, which helps connect performance with running-cost expectations."

    if isinstance(power, (int, float)) and power >= 600:
        role = "high-output performance car"
    elif isinstance(power, (int, float)) and power >= 350:
        role = "strong performance choice"
    elif engine and re.search(r"kwh|electric|ev", engine, re.I):
        role = "electric vehicle candidate"
    else:
        role = "vehicle shortlist candidate"

    sections = [
        {
            "heading": "Performance interpretation",
            "paragraphs": [
                f"The headline numbers make {name} a {role}. Horsepower explains the available output, but the way that output feels depends on gearing, traction, tire setup, weight, and the shape of the power curve.",
                "Use the figures on this page as a first filter. A stronger number is useful only when it supports the way the car will be driven, whether that means daily overtaking, long-distance cruising, occasional spirited driving, or track-focused use.",
            ],
        },
        {
            "heading": "Ownership context",
            "paragraphs": [
                "A complete buying decision should include more than acceleration and top speed. Fuel or charging cost, insurance, tires, maintenance, depreciation, and local taxes can change the value case quickly.",
                f"If {name} is being compared with another model, check both the performance table and the running-cost details. A car can be quicker on paper while still being the weaker ownership fit if it costs more to fuel, insure, or maintain.",
            ],
        },
        {
            "heading": "Who should consider it",
            "paragraphs": [
                f"{name} makes the most sense for shoppers who want its specific balance of performance, price, engine character, and usability. It should be compared with vehicles in a similar body style and price band before drawing a final conclusion.",
                "For final purchase research, confirm the exact market version, trim level, tire package, and model-year specification from the seller or manufacturer. Published figures can vary by market and equipment.",
            ],
        },
    ]

    bullets = [
        "Compare it against models with a similar price and body style.",
        "Read acceleration together with power, top speed, and traction layout.",
        "Add yearly fuel or charging cost before judging value.",
        "Confirm local trim details before making a purchase decision.",
    ]

    return {"summary": summary, "sections": sections, "bullets": bullets}


def build_article_context(items, article_sections, slug, section_label, section_path):
    item = next((entry for entry in items if entry.get("slug") == slug), None)
    if not item:
        return None
    sections = article_sections.get(slug)
    if not sections:
        return None
    return {
        "slug": slug,
        "section_label": section_label,
        "section_path": section_path,
        "title": item.get("title_en") or "CarQuantix article",
        "summary": item.get("summary_en") or "",
        "tag": item.get("tag_en") or section_label,
        "sections": sections,
    }


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


def build_indexable_car_slugs(cars):
    return {entry["slug"] for entry in select_featured_car_links(build_car_links(cars)) if entry.get("slug")}


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


def strip_vehicle_year(name):
    return re.sub(r"^\s*(?:19|20)\d{2}\s+", "", str(name or "")).strip()


def get_compare_seo_override(car_a, car_b):
    compare_slug = build_compare_slug(car_a, car_b)
    return COMPARE_SEO_OVERRIDES.get(compare_slug) or {}


def get_compare_display_names(car_a, car_b):
    return (
        strip_vehicle_year(car_a.get("name")) or str(car_a.get("name") or "Car A").strip(),
        strip_vehicle_year(car_b.get("name")) or str(car_b.get("name") or "Car B").strip(),
    )


def build_compare_page_title(car_a, car_b):
    override = get_compare_seo_override(car_a, car_b)
    if override.get("title"):
        return override["title"]

    left_name, right_name = get_compare_display_names(car_a, car_b)
    body_style = f"{left_name} vs {right_name}"
    name_text = f"{left_name} {right_name}".lower()
    if re.search(r"\bx[1-7]\b|q[2-8]\b|gl[acse]|gle|glc|lx|nx|rx|suv|cayenne|macan|range rover", name_text):
        return f"{body_style}: Luxury SUV Comparison, Price, Comfort and Reliability"
    if re.search(r"ferrari|mclaren|lamborghini|porsche 911|jaguar f-type|corvette|r8|amg gt", name_text):
        return f"{body_style}: Speed, Price, Reliability and Driving Experience"
    return f"{body_style}: Performance, Price, Reliability and Daily Driving"


def build_compare_quick_verdict(car_a, car_b, compare_decision):
    override = get_compare_seo_override(car_a, car_b)
    if override.get("quick_verdict"):
        return override["quick_verdict"]

    left_name, right_name = get_compare_display_names(car_a, car_b)
    overall = next(
        (
            item
            for item in (compare_decision or {}).get("verdict_items", [])
            if item.get("label") == "Overall winner"
        ),
        None,
    )
    winner = str((overall or {}).get("winner") or "").strip()
    if winner and winner not in {"Too close to call", left_name, right_name}:
        winner = strip_vehicle_year(winner)
    if winner and winner not in {"Too close to call", ""}:
        other = right_name if winner == left_name else left_name
        return (
            f"The {winner} is the better pick if you want the strongest overall spec balance in this matchup, "
            f"while the {other} can still make more sense if its price, comfort or daily-use character fits your priorities better."
        )
    return (
        f"The {left_name} vs {right_name} decision is close, so the better choice depends on whether you value performance, "
        "price, comfort, reliability or daily driving more."
    )


def build_compare_content_sections(car_a, car_b, compare_decision):
    left_name, right_name = get_compare_display_names(car_a, car_b)
    left_price = format_display_price(car_a.get("price"))
    right_price = format_display_price(car_b.get("price"))
    left_consumption = car_a.get("consumption") or {}
    right_consumption = car_b.get("consumption") or {}
    quick_verdict = build_compare_quick_verdict(car_a, car_b, compare_decision)

    sections = [
        {
            "heading": "Quick Verdict",
            "body": quick_verdict,
        },
        {
            "heading": "Performance Comparison",
            "body": (
                f"For performance, compare power, 0-100 km/h acceleration and top speed together. "
                f"{left_name} records {car_a.get('power', '-')} hp, {car_a.get('acc', '-')} seconds to 100 km/h and {car_a.get('topSpeed', '-')} km/h, "
                f"while {right_name} records {car_b.get('power', '-')} hp, {car_b.get('acc', '-')} seconds and {car_b.get('topSpeed', '-')} km/h."
            ),
        },
        {
            "heading": "Price and Value",
            "body": (
                f"Price changes the answer because a quicker car is not always the better buy. "
                f"{left_name} is listed at {left_price}, while {right_name} is listed at {right_price}. "
                "Use the price gap together with performance and equipment to judge real value."
            ),
        },
        {
            "heading": "Interior and Comfort",
            "body": (
                f"Interior and comfort matter most if this will be a daily car. "
                f"{left_name} and {right_name} should be judged by seating position, cabin space, ride quality, visibility, infotainment and long-distance refinement, not only by acceleration numbers."
            ),
        },
        {
            "heading": "Reliability",
            "body": (
                "Reliability is best judged by ownership history, service records and common repair patterns for each model. "
                f"Before choosing between {left_name} and {right_name}, check known issues, warranty coverage and how easily each car can be serviced where you live."
            ),
        },
        {
            "heading": "Maintenance Cost",
            "body": (
                "Maintenance cost can outweigh a small purchase-price difference. "
                f"For {left_name} vs {right_name}, compare scheduled servicing, tires, brakes, insurance, parts availability and depreciation before deciding which one is cheaper to own."
            ),
        },
        {
            "heading": "Fuel Economy",
            "body": (
                f"Fuel economy is part of the long-term cost picture. "
                f"{left_name} is rated at {left_consumption.get('value', '-')} {left_consumption.get('unit', '')}, "
                f"while {right_name} is rated at {right_consumption.get('value', '-')} {right_consumption.get('unit', '')}. "
                "For high-mileage drivers, even a small efficiency difference can matter."
            ),
        },
        {
            "heading": "Daily Driving",
            "body": (
                f"For daily driving, the better choice is the one that feels easier to live with. "
                f"Compare {left_name} and {right_name} by ride comfort, parking ease, cargo space, fuel use, road noise and how relaxed each car feels in traffic."
            ),
        },
        {
            "heading": "Which One Should You Buy?",
            "body": quick_verdict,
        },
    ]

    reverse_keyword = get_compare_seo_override(car_a, car_b).get("reverse_keyword")
    if reverse_keyword:
        sections.insert(
            1,
            {
                "heading": reverse_keyword,
                "body": (
                    f"People also search for {reverse_keyword}. This is the same comparison as {left_name} vs {right_name}, "
                    "so this canonical page keeps both search directions in one stronger result."
                ),
            },
        )

    return sections


def build_compare_faq(car_a, car_b, compare_decision):
    left_name, right_name = get_compare_display_names(car_a, car_b)
    quick_verdict = build_compare_quick_verdict(car_a, car_b, compare_decision)
    return [
        {
            "question": f"Which is better, {left_name} or {right_name}?",
            "answer": quick_verdict,
        },
        {
            "question": f"Which is faster, {left_name} or {right_name}?",
            "answer": (
                f"Compare horsepower, 0-100 km/h and top speed together. "
                f"{left_name} has {car_a.get('power', '-')} hp and a {car_a.get('topSpeed', '-')} km/h top speed, "
                f"while {right_name} has {car_b.get('power', '-')} hp and a {car_b.get('topSpeed', '-')} km/h top speed."
            ),
        },
        {
            "question": f"Which is better for daily driving?",
            "answer": (
                f"For daily driving, compare comfort, running cost, visibility, cabin space and reliability. "
                f"The better daily choice between {left_name} and {right_name} depends on those ownership priorities more than headline speed alone."
            ),
        },
    ]


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

    buyer_recommendations = []
    for side, name, car, pros in (
        ("left", left_name, car_a, left_pros),
        ("right", right_name, car_b, right_pros),
    ):
        reasons = []
        if price_winner == side:
            reasons.append("a lower listed price")
        if power_winner == side:
            reasons.append("stronger horsepower")
        if acc_winner == side:
            reasons.append("quicker 0-100 km/h acceleration")
        if top_speed_winner == side:
            reasons.append("a higher top speed")
        if consumption_winner == side:
            reasons.append("better recorded efficiency")
        if year_winner == side:
            reasons.append("a newer model year")

        engine_text = str(car.get("engine") or "").strip()
        if engine_text:
            lower_engine = engine_text.lower()
            if re.search(r"\bv8\b|shelby|hemi|mustang|camaro|challenger", lower_engine):
                reasons.append("classic muscle-car character")
            elif re.search(r"electric|ev|kwh", lower_engine):
                reasons.append("electric powertrain response")
            elif re.search(r"hybrid", lower_engine):
                reasons.append("hybrid powertrain flexibility")
            elif re.search(r"xdrive|quattro|4matic|awd|4wd", lower_engine):
                reasons.append("all-wheel-drive traction")
            elif engine_text:
                reasons.append(f"its {engine_text} powertrain")

        if not reasons:
            reasons = pros[:2] or ["its overall spec balance"]

        buyer_recommendations.append(
            {
                "name": name,
                "lead": f"Choose the {name} if:",
                "reason": (
                    "You prioritize "
                    f"{join_compare_labels(reasons[:3])}."
                ),
            }
        )

    return {
        "verdict_items": verdict_items,
        "buyer_recommendations": buyer_recommendations,
        "left": {
            "pros": left_pros[:3],
            "cons": left_cons[:3],
        },
        "right": {
            "pros": right_pros[:3],
            "cons": right_cons[:3],
        },
    }


def build_featured_compare_links(cars, slug_map, limit=FEATURED_COMPARE_LIMIT):
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
                "title": build_compare_page_title(left_car, right_car),
                "left_car": left_car,
                "right_car": right_car,
            }
        )
        if limit and len(links) >= limit:
            break
    return links


MULTI_BRAND_PREFIXES = (
    "alfa romeo",
    "aston martin",
    "land rover",
    "range rover",
    "rolls royce",
    "mercedes-benz",
    "mercedes benz",
)


def get_vehicle_slug(car):
    return str((car or {}).get("slug") or "").strip()


def get_vehicle_name(car):
    return str((car or {}).get("name") or (car or {}).get("id") or "Vehicle").strip()


def get_vehicle_brand(car):
    name = re.sub(r"^\d{4}\s+", "", get_vehicle_name(car)).strip()
    if not name:
        return "Other"
    lower = name.lower()
    for prefix in MULTI_BRAND_PREFIXES:
        if lower.startswith(prefix):
            return name[:len(prefix)]
    return name.split()[0]


def get_vehicle_year(car):
    match = re.match(r"^(\d{4})\s+", get_vehicle_name(car))
    return int(match.group(1)) if match else None


def numeric_or_none(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_car_link_entry(car):
    slug = get_vehicle_slug(car)
    if not slug:
        return None
    return {"href": f"/cars/{slug}", "title": get_vehicle_name(car)}


def unique_link_entries(entries, limit=None):
    result = []
    seen = set()
    for entry in entries:
        if not entry:
            continue
        href = str(entry.get("href") or "").strip()
        title = str(entry.get("title") or "").strip()
        if not href or not title or href in seen:
            continue
        seen.add(href)
        result.append({"href": href, "title": title})
        if limit and len(result) >= limit:
            break
    return result


def related_car_score(target_car, candidate):
    target_brand = get_vehicle_brand(target_car).lower()
    candidate_brand = get_vehicle_brand(candidate).lower()
    score = 0.0
    if target_brand and target_brand == candidate_brand:
        score += 1000

    target_power = numeric_or_none((target_car or {}).get("power"))
    candidate_power = numeric_or_none((candidate or {}).get("power"))
    if target_power is not None and candidate_power is not None:
        score -= abs(target_power - candidate_power) / 4

    target_acc = numeric_or_none((target_car or {}).get("acc"))
    candidate_acc = numeric_or_none((candidate or {}).get("acc"))
    if target_acc is not None and candidate_acc is not None:
        score -= abs(target_acc - candidate_acc) * 18

    target_speed = numeric_or_none((target_car or {}).get("topSpeed"))
    candidate_speed = numeric_or_none((candidate or {}).get("topSpeed"))
    if target_speed is not None and candidate_speed is not None:
        score -= abs(target_speed - candidate_speed) / 6

    target_year = get_vehicle_year(target_car)
    candidate_year = get_vehicle_year(candidate)
    if target_year and candidate_year:
        score -= abs(target_year - candidate_year) * 2

    return score


def build_related_car_links(car, cars, limit=8):
    current_slug = get_vehicle_slug(car)
    candidates = [entry for entry in cars if get_vehicle_slug(entry) and get_vehicle_slug(entry) != current_slug]
    ordered = sorted(
        candidates,
        key=lambda entry: (related_car_score(car, entry), get_vehicle_name(entry)),
        reverse=True,
    )
    return unique_link_entries((build_car_link_entry(entry) for entry in ordered), limit=limit)


def build_related_article_links(current_slug=None, limit=8):
    articles = [
        {"href": f"/guides/{item['slug']}", "title": item.get("title_en") or item["slug"]}
        for item in GUIDE_ITEMS
        if item.get("slug")
    ] + [
        {"href": f"/blog/{item['slug']}", "title": item.get("title_en") or item["slug"]}
        for item in BLOG_ITEMS
        if item.get("slug")
    ]
    if current_slug:
        current_index = next((index for index, item in enumerate(articles) if item["href"].endswith(f"/{current_slug}")), -1)
        articles = articles[current_index + 1:] + articles[:current_index] if current_index >= 0 else articles
    return unique_link_entries(articles, limit=limit)


def build_editorial_car_links(cars, limit=8):
    return unique_link_entries(
        (
            {"href": f"/cars/{entry['slug']}", "title": entry["name"]}
            for entry in select_featured_car_links(build_car_links(cars))
            if entry.get("slug")
        ),
        limit=limit,
    )


def build_editorial_compare_links(cars, slug_map, limit=8):
    return unique_link_entries(
        (
            {"href": entry.get("href"), "title": entry.get("title")}
            for entry in build_featured_compare_links(cars, slug_map, limit=None)
        ),
        limit=limit,
    )


def compare_entry_car_slugs(entry):
    return {
        get_vehicle_slug(entry.get("left_car")),
        get_vehicle_slug(entry.get("right_car")),
    } - {""}


def compare_entry_brands(entry):
    return {
        get_vehicle_brand(entry.get("left_car")).lower(),
        get_vehicle_brand(entry.get("right_car")).lower(),
    } - {""}


def build_related_compare_links_for_car(car, cars, slug_map, limit=8, exclude_href=None):
    target_slug = get_vehicle_slug(car)
    target_brand = get_vehicle_brand(car).lower()
    scored = []
    popular = []
    for entry in build_featured_compare_links(cars, slug_map, limit=None):
        href = str(entry.get("href") or "")
        if not href or href == exclude_href:
            continue
        link = {"href": href, "title": entry.get("title")}
        popular.append(link)
        slugs = compare_entry_car_slugs(entry)
        brands = compare_entry_brands(entry)
        score = 0
        if target_slug and target_slug in slugs:
            score += 1000
        if target_brand and target_brand in brands:
            score += 150
        if score:
            scored.append((score, link))
    ordered = [link for _, link in sorted(scored, key=lambda item: item[0], reverse=True)]
    return unique_link_entries(ordered + popular, limit=limit)


def build_related_compare_links_for_pair(left_car, right_car, cars, slug_map, limit=8, exclude_href=None):
    override = get_compare_seo_override(left_car, right_car)
    override_links = []
    for entry in override.get("related_compare_links") or []:
        if len(entry) != 3:
            continue
        title, left_ref, right_ref = entry
        override_left = resolve_car_reference(left_ref, cars, slug_map)
        override_right = resolve_car_reference(right_ref, cars, slug_map)
        if not override_left or not override_right:
            continue
        href = build_compare_href(override_left, override_right)
        if href and href != exclude_href:
            override_links.append({"href": href, "title": title})
    override_links.extend(override.get("extra_links") or [])

    target_slugs = {get_vehicle_slug(left_car), get_vehicle_slug(right_car)} - {""}
    target_brands = {get_vehicle_brand(left_car).lower(), get_vehicle_brand(right_car).lower()} - {""}
    scored = []
    popular = []
    for entry in build_featured_compare_links(cars, slug_map, limit=None):
        href = str(entry.get("href") or "")
        if not href or href == exclude_href:
            continue
        link = {"href": href, "title": entry.get("title")}
        popular.append(link)
        score = 0
        score += 1000 * len(target_slugs & compare_entry_car_slugs(entry))
        score += 150 * len(target_brands & compare_entry_brands(entry))
        if score:
            scored.append((score, link))
    ordered = [link for _, link in sorted(scored, key=lambda item: item[0], reverse=True)]
    return unique_link_entries(override_links + ordered + popular, limit=limit)


def build_indexable_compare_slugs(cars, slug_map):
    slugs = set()
    for entry in build_featured_compare_links(cars, slug_map):
        href = str(entry.get("href") or "")
        if href.startswith("/compare/"):
            slugs.add(href.rsplit("/", 1)[-1])
    return slugs


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
    ensure_db_ready()
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


def get_comments_for_page(page, comments=None):
    page = get_comment_page(page)
    source_comments = load_comments() if comments is None else comments
    return [comment for comment in source_comments if comment.get("page", "home") == page]


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
    changed = False
    defaults_by_id = {item["id"]: _normalize_comment(item) for item in DEFAULT_COMMENTS}
    for item in raw_comments:
        if isinstance(item, dict) and str(item.get("id") or "").startswith("seed_"):
            changed = True
            continue
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

    changed = changed or comments != raw_comments
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


def clean_listing_text(value, max_length=120):
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    return value[:max_length]


def clean_listing_multiline(value, max_length=800):
    value = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value[:max_length]


def normalize_listing_currency(value):
    raw_value = clean_listing_text(value, 40).upper()
    raw_value = re.sub(r"[^A-Z ]", "", raw_value)
    code = LISTING_CURRENCY_ALIASES.get(raw_value, raw_value)
    return code if code in LISTING_CURRENCY_BY_CODE else ""


def format_listing_location(city="", country="", street="", postal_code=""):
    city = clean_listing_text(city, 80)
    country = clean_listing_text(country, 80)
    street = clean_listing_text(street, 120)
    postal_code = clean_listing_text(postal_code, 30)
    city_line = ", ".join(part for part in (postal_code, city) if part)
    location_parts = [part for part in (street, city_line, country) if part]
    return ", ".join(location_parts)[:160]


def normalize_listing(item):
    if not isinstance(item, dict):
        item = {}
    created_at = clean_listing_text(item.get("created_at"), 40)
    if not created_at:
        created_at = datetime.utcnow().strftime("%Y-%m-%d")
    price = clean_listing_text(item.get("price"), 40)
    price_currency = normalize_listing_currency(item.get("price_currency") or item.get("currency"))
    price_currency_display = LISTING_CURRENCY_BY_CODE.get(price_currency, {}).get("display", "")
    price_currency_symbol = LISTING_CURRENCY_SYMBOLS.get(price_currency, price_currency_display)
    old_price = clean_listing_text(item.get("old_price"), 40)
    mileage = clean_listing_text(item.get("mileage"), 40)
    image_url = clean_listing_text(item.get("image_url"), 300)
    if image_url and not (re.match(r"^https?://", image_url, re.IGNORECASE) or image_url.startswith("/listing-uploads/")):
        image_url = ""
    images = item.get("images") if isinstance(item.get("images"), list) else []
    images = [
        clean_listing_text(image, 300)
        for image in images
        if clean_listing_text(image, 300).startswith("/listing-uploads/")
        or re.match(r"^https?://", clean_listing_text(image, 300), re.IGNORECASE)
    ]
    if image_url and image_url not in images:
        images.insert(0, image_url)

    return {
        "id": clean_listing_text(item.get("id"), 40) or secrets.token_hex(8),
        "created_at": created_at,
        "owner_email": clean_listing_text(item.get("owner_email"), 120).lower(),
        "seller_name": clean_listing_text(item.get("seller_name"), 80),
        "email": clean_listing_text(item.get("email"), 120),
        "phone": clean_listing_text(item.get("phone"), 40),
        "country": clean_listing_text(item.get("country"), 80),
        "street": clean_listing_text(item.get("street"), 120),
        "postal_code": clean_listing_text(item.get("postal_code"), 30),
        "city": clean_listing_text(item.get("city"), 160),
        "make": clean_listing_text(item.get("make"), 60),
        "model": clean_listing_text(item.get("model"), 80),
        "year": clean_listing_text(item.get("year"), 10),
        "mileage": mileage,
        "price": price,
        "price_currency": price_currency,
        "price_currency_display": price_currency_display,
        "price_currency_symbol": price_currency_symbol,
        "old_price": old_price,
        "fuel": clean_listing_text(item.get("fuel"), 40),
        "consumption": clean_listing_text(item.get("consumption"), 40),
        "image_url": image_url or (images[0] if images else ""),
        "images": images[:LISTING_IMAGE_LIMIT],
        "description": clean_listing_multiline(item.get("description"), 800),
        "status": clean_listing_text(item.get("status"), 20) or "active",
    }


def load_car_listings(include_inactive=False):
    db_listings = load_car_listings_from_db(include_inactive=include_inactive)
    if db_listings is not None:
        return db_listings

    raw_listings = []
    if CAR_LISTINGS_PATH.exists():
        try:
            parsed = json.loads(CAR_LISTINGS_PATH.read_text(encoding="utf-8"))
            if isinstance(parsed, list):
                raw_listings = parsed
        except json.JSONDecodeError:
            raw_listings = []

    listings = []
    seen_ids = set()
    changed = False
    for item in raw_listings:
        normalized = normalize_listing(item)
        if normalized["id"] in seen_ids:
            changed = True
            continue
        if not normalized["make"] or not normalized["model"] or not normalized["year"]:
            changed = True
            continue
        if include_inactive or normalized["status"] == "active":
            listings.append(normalized)
        seen_ids.add(normalized["id"])

    listings.sort(key=lambda item: item.get("created_at", ""), reverse=True)
    if changed:
        save_car_listings(listings)
    return listings


def save_car_listings(listings):
    if save_car_listings_to_db(listings):
        return
    ensure_parent_dir(CAR_LISTINGS_PATH)
    CAR_LISTINGS_PATH.write_text(json.dumps(listings, indent=2), encoding="utf-8")


def init_listing_db():
    if not db_enabled():
        return
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS car_listings (
                        id TEXT PRIMARY KEY,
                        payload TEXT NOT NULL,
                        created_at TEXT,
                        status TEXT NOT NULL DEFAULT 'active',
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
                cur.execute("CREATE INDEX IF NOT EXISTS idx_car_listings_created_at ON car_listings (created_at DESC)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_car_listings_status ON car_listings (status)")
    except Exception as exc:
        disable_db_runtime(f"listing db init failed: {exc}")


def load_car_listings_from_db(include_inactive=False):
    if not db_enabled():
        return None
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                if include_inactive:
                    cur.execute("SELECT payload FROM car_listings ORDER BY created_at DESC, updated_at DESC")
                else:
                    cur.execute("SELECT payload FROM car_listings WHERE status = 'active' ORDER BY created_at DESC, updated_at DESC")
                listings = []
                changed = False
                seen_ids = set()
                for row in cur.fetchall():
                    try:
                        item = json.loads(row["payload"])
                    except (TypeError, json.JSONDecodeError):
                        changed = True
                        continue
                    normalized = normalize_listing(item)
                    if not include_inactive and normalized.get("status") != "active":
                        changed = True
                        continue
                    if normalized["id"] in seen_ids:
                        changed = True
                        continue
                    seen_ids.add(normalized["id"])
                    listings.append(normalized)
                if changed:
                    save_car_listings_to_db(listings)
                return listings
    except Exception as exc:
        disable_db_runtime(f"listing db load failed: {exc}")
        return None


def save_car_listings_to_db(listings):
    if not db_enabled():
        return False
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM car_listings")
                for listing in listings:
                    clean_listing = {key: value for key, value in listing.items() if not key.startswith("_")}
                    listing_id = clean_listing_text(clean_listing.get("id"), 40)
                    if not listing_id:
                        continue
                    cur.execute(
                        """
                        INSERT INTO car_listings (id, payload, created_at, status)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            listing_id,
                            json.dumps(clean_listing),
                            clean_listing_text(clean_listing.get("created_at"), 40),
                            clean_listing_text(clean_listing.get("status"), 20) or "active",
                        ),
                    )
        return True
    except Exception as exc:
        disable_db_runtime(f"listing db save failed: {exc}")
        return False


def migrate_json_car_listings_to_db():
    if not db_enabled() or not CAR_LISTINGS_PATH.exists():
        return
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS count FROM car_listings")
                if int(cur.fetchone()["count"] or 0) > 0:
                    return
    except Exception as exc:
        disable_db_runtime(f"listing db migration count failed: {exc}")
        return

    try:
        parsed = json.loads(CAR_LISTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    if isinstance(parsed, list):
        listings = [normalize_listing(item) for item in parsed]
        if listings:
            save_car_listings_to_db(listings)


def save_listing_images(files):
    uploaded = []
    if not files:
        return uploaded, ""
    image_files = [file for file in files.getlist("images") if file and file.filename]
    if len(image_files) > LISTING_IMAGE_LIMIT:
        return [], f"Please upload no more than {LISTING_IMAGE_LIMIT} images."

    LISTING_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in image_files:
        original_name = secure_filename(image_file.filename or "")
        extension = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
        if extension not in LISTING_IMAGE_EXTENSIONS:
            return [], "Images must be JPG, PNG, WebP or GIF files."
        if image_file.mimetype and image_file.mimetype not in LISTING_IMAGE_MIME_TYPES:
            return [], "Images must be JPG, PNG, WebP or GIF files."
        filename = f"{int(time.time())}_{secrets.token_hex(5)}.{extension}"
        image_file.save(LISTING_UPLOAD_DIR / filename)
        uploaded.append(f"/listing-uploads/{filename}")
    return uploaded, ""


def validate_listing_form(form, files=None):
    honeypot = clean_listing_text(form.get("website"), 80)
    if honeypot:
        return None, "Listing could not be submitted."

    country = clean_listing_text(form.get("country"), 80)
    city = clean_listing_text(form.get("city"), 80)
    street = clean_listing_text(form.get("street"), 120)
    postal_code = clean_listing_text(form.get("postal_code"), 30)
    location = format_listing_location(city=city, country=country, street=street, postal_code=postal_code)

    listing = normalize_listing(
        {
            "id": f"listing_{int(time.time())}_{secrets.token_hex(4)}",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
            "seller_name": form.get("seller_name"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "country": country,
            "street": street,
            "postal_code": postal_code,
            "city": location,
            "make": form.get("make"),
            "model": form.get("model"),
            "year": form.get("year"),
            "mileage": form.get("mileage"),
            "price": form.get("price"),
            "price_currency": form.get("price_currency"),
            "fuel": form.get("fuel"),
            "description": form.get("description"),
            "status": "active",
        }
    )

    required_fields = ("seller_name", "city", "make", "model", "year", "mileage", "price", "description")
    if any(not listing.get(field) for field in required_fields):
        return None, "Please fill in all required fields."
    if not listing["country"] or listing["country"] not in LISTING_COUNTRIES:
        return None, "Please select a valid country."
    if not city:
        return None, "Please add the city or region."
    if not listing["email"] and not listing["phone"]:
        return None, "Please add at least one contact option: email or phone."
    if listing["email"] and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", listing["email"]):
        return None, "Please enter a valid email address."
    if listing["fuel"] and listing["fuel"] not in LISTING_FUEL_TYPES:
        return None, "Please select a valid fuel type."
    if not listing["price_currency"]:
        return None, "Please select a valid currency."
    if not re.match(r"^(19|20)\d{2}$", listing["year"]):
        return None, "Please enter a valid model year."
    current_year = datetime.utcnow().year + 1
    if int(listing["year"]) < 1950 or int(listing["year"]) > current_year:
        return None, "Please enter a realistic model year."

    uploaded_images, upload_error = save_listing_images(files)
    if upload_error:
        return None, upload_error
    listing["images"] = uploaded_images
    listing["image_url"] = uploaded_images[0] if uploaded_images else ""

    return listing, ""


def get_session_listing_ids():
    my_listing_ids = session.get("my_listing_ids")
    if not isinstance(my_listing_ids, list):
        return []
    return [clean_listing_text(listing_id, 40) for listing_id in my_listing_ids if clean_listing_text(listing_id, 40)]


def get_current_user_email():
    user = session.get("user") or {}
    return clean_listing_text(user.get("email"), 120).lower()


def get_listing_owner_email(listing):
    if not listing:
        return ""
    return clean_listing_text(listing.get("owner_email") or listing.get("email"), 120).lower()


def user_can_manage_listing(listing):
    if not listing:
        return False
    listing_id = clean_listing_text(listing.get("id"), 40)
    if listing_id and listing_id in set(get_session_listing_ids()):
        return True
    current_user_email = get_current_user_email()
    return bool(current_user_email and get_listing_owner_email(listing) == current_user_email)


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
        init_listing_db()
        migrate_json_users_to_db()
        migrate_json_car_listings_to_db()
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


@app.route("/listing-uploads/<path:filename>")
def listing_upload(filename):
    return send_from_directory(LISTING_UPLOAD_DIR, filename)


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
    search_query = str(request.args.get("q") or "").strip()
    if search_query:
        parsed_query = urllib.parse.urlparse(search_query)
        query_path = parsed_query.path if parsed_query.scheme or parsed_query.netloc else search_query
        normalized_query = re.sub(r"\s+", "-", query_path.strip().lower()).strip("/")
        if normalized_query.startswith("compare/"):
            normalized_query = normalized_query[len("compare/"):]
        if "-vs-" in normalized_query:
            resolved = resolve_compare_slug(normalized_query, slug_map)
            if resolved:
                return redirect(f"/compare/{resolved['canonical_slug']}", code=302)
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
        meta_description="Read CarQuantix automotive editorials, car buying context, performance explainers and practical notes for comparing vehicles more clearly.",
        robots_directive="index,follow",
    )


@app.route("/guides/<slug>")
def guide_article(slug):
    article = build_article_context(GUIDE_ITEMS, GUIDE_ARTICLE_SECTIONS, slug, "Guides", "/guides")
    if not article:
        return "Not Found", 404
    cars, slug_map = load_cars()
    canonical_url = f"{get_base_url()}/guides/{article['slug']}"
    meta_title = f"{article['title']} - CarQuantix Guides"
    page_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["summary"],
        "url": canonical_url,
        "publisher": {"@type": "Organization", "name": "CarQuantix"},
    }
    return render_template(
        "article_detail.html",
        article=article,
        canonical_url=canonical_url,
        meta_title=meta_title,
        meta_description=article["summary"],
        robots_directive="index,follow",
        page_schema=page_schema,
        related_article_links=build_related_article_links(article["slug"], limit=8),
        related_car_links=build_editorial_car_links(cars, limit=8),
        related_compare_links=build_editorial_compare_links(cars, slug_map, limit=8),
    )


@app.route("/blog/<slug>")
def blog_article(slug):
    article = build_article_context(BLOG_ITEMS, BLOG_ARTICLE_SECTIONS, slug, "Blog", "/blog")
    if not article:
        return "Not Found", 404
    cars, slug_map = load_cars()
    canonical_url = f"{get_base_url()}/blog/{article['slug']}"
    meta_title = f"{article['title']} - CarQuantix Blog"
    page_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["summary"],
        "url": canonical_url,
        "publisher": {"@type": "Organization", "name": "CarQuantix"},
    }
    return render_template(
        "article_detail.html",
        article=article,
        canonical_url=canonical_url,
        meta_title=meta_title,
        meta_description=article["summary"],
        robots_directive="index,follow",
        page_schema=page_schema,
        related_article_links=build_related_article_links(article["slug"], limit=8),
        related_car_links=build_editorial_car_links(cars, limit=8),
        related_compare_links=build_editorial_compare_links(cars, slug_map, limit=8),
    )


@app.route("/methodology")
def methodology():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "methodology.html",
        canonical_url=canonical_url,
        meta_title="Methodology and Data Notes - CarQuantix",
        meta_description="See how CarQuantix compares vehicle performance, fuel consumption, pricing and ownership context with clear methods and practical data notes.",
        robots_directive="index,follow",
    )


@app.route("/privacy-policy")
def privacy_policy():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "privacy_policy.html",
        canonical_url=canonical_url,
        meta_title="CarQuantix Privacy Policy",
        meta_description="Read how CarQuantix collects, uses and protects your data, including privacy practices for accounts, analytics, subscriptions and site features.",
        robots_directive="index,follow",
    )


@app.route("/about-us")
def about_us():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "about_us.html",
        canonical_url=canonical_url,
        meta_title="About Us - CarQuantix",
        meta_description="Learn how CarQuantix helps drivers compare cars with horsepower, acceleration, top speed, pricing, fuel use and practical ownership context.",
        robots_directive="index,follow",
    )


@app.route("/contact")
def contact():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "contact.html",
        canonical_url=canonical_url,
        meta_title="Contact - CarQuantix",
        meta_description="Contact the CarQuantix team for product support, data questions, business inquiries, partnerships, media requests or account assistance.",
        robots_directive="index,follow",
    )


@app.route("/sell-car", methods=["GET", "POST"])
def sell_car():
    session.permanent = True
    message = ""
    error = ""
    form_values = {}
    active_listing_view = request.args.get("view") if request.args.get("view") in {"all", "mine"} else "all"
    if request.args.get("removed") == "1":
        message = "Your listing was removed."
    if request.method == "POST":
        form_values = request.form.to_dict()
        listing, error = validate_listing_form(request.form, request.files)
        if listing and not error:
            current_user_email = get_current_user_email()
            if current_user_email:
                listing["owner_email"] = current_user_email
            listings = load_car_listings(include_inactive=True)
            listings.insert(0, listing)
            save_car_listings(listings)
            my_listing_ids = session.get("my_listing_ids")
            if not isinstance(my_listing_ids, list):
                my_listing_ids = []
            if listing["id"] not in my_listing_ids:
                my_listing_ids.insert(0, listing["id"])
            session["my_listing_ids"] = my_listing_ids[:100]
            message = "Your car is now live for sale."
            form_values = {}
            active_listing_view = "mine"

    listings = load_car_listings()
    for index, listing in enumerate(listings):
        listing["_list_index"] = index
    current_user_email = get_current_user_email()
    my_listing_ids = session.get("my_listing_ids")
    if not isinstance(my_listing_ids, list):
        my_listing_ids = []
    my_listing_id_set = {clean_listing_text(listing_id, 40) for listing_id in my_listing_ids}
    my_listings = [
        listing
        for listing in listings
        if listing.get("id") in my_listing_id_set
        or (current_user_email and get_listing_owner_email(listing) == current_user_email)
    ]
    canonical_url = f"{get_base_url()}{request.path}"
    page_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Sell Your Car - CarQuantix",
        "description": "Sell your car and browse public vehicle listings on CarQuantix.",
        "url": canonical_url,
    }
    return render_template(
        "sell_car.html",
        listings=listings,
        my_listings=my_listings,
        current_user_email=current_user_email,
        active_listing_view=active_listing_view,
        countries=LISTING_COUNTRIES,
        currencies=[
            {"code": code, "display": display, "name": name}
            for code, display, name in LISTING_CURRENCIES
        ],
        message=message,
        error=error,
        form_values=form_values,
        canonical_url=canonical_url,
        meta_title="Sell Your Car Online - CarQuantix",
        meta_description="Sell your car on CarQuantix and browse public vehicle listings with price, mileage, city and seller contact details.",
        robots_directive="index,follow",
        page_schema=page_schema,
    )


@app.route("/sell-car/delete/<listing_id>", methods=["POST"])
def delete_car_listing(listing_id):
    listing_id = clean_listing_text(listing_id, 40)
    listings = load_car_listings(include_inactive=True)
    listing = next((item for item in listings if item.get("id") == listing_id), None)
    if not listing or not user_can_manage_listing(listing):
        return redirect(url_for("sell_car"))

    listings = [item for item in listings if item.get("id") != listing_id]
    save_car_listings(listings)

    my_listing_ids = [item_id for item_id in get_session_listing_ids() if item_id != listing_id]
    session["my_listing_ids"] = my_listing_ids
    return redirect(url_for("sell_car", view="mine", removed="1"))


@app.route("/pricing")
def pricing():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "pricing.html",
        canonical_url=canonical_url,
        meta_title="Pricing - CarQuantix",
        meta_description="Review CarQuantix pricing, subscription plans, account features and comparison tools for researching vehicle performance and ownership costs.",
        robots_directive="index,follow",
    )


@app.route("/terms")
def terms():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "terms.html",
        canonical_url=canonical_url,
        meta_title="Terms and Conditions - CarQuantix",
        meta_description="Read the CarQuantix terms and conditions covering website use, accounts, subscriptions, vehicle data, content rights and service limitations.",
        robots_directive="index,follow",
    )


@app.route("/refund-policy")
def refund_policy():
    canonical_url = f"{get_base_url()}{request.path}"
    return render_template(
        "refund_policy.html",
        canonical_url=canonical_url,
        meta_title="Refund Policy - CarQuantix",
        meta_description="Review the CarQuantix refund policy for subscriptions and digital services, including eligibility, timing, billing issues and support steps.",
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
    cars, slug_map = load_cars()
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
    is_indexable = canonical_slug in build_indexable_car_slugs(cars)
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
        car_content=build_car_detail_content(car),
        meta_title=meta_title,
        meta_description=meta_description,
        canonical_url=canonical_url,
        robots_directive="index,follow",
        adsense_enabled=is_indexable,
        page_schema=page_schema,
        related_car_links=build_related_car_links(car, cars, limit=8),
        related_compare_links=build_related_compare_links_for_car(car, cars, slug_map, limit=8),
        related_article_links=build_related_article_links(limit=6),
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
    compare_page_title = build_compare_page_title(left_car, right_car)
    compare_quick_verdict = build_compare_quick_verdict(left_car, right_car, compare_decision)
    compare_sections = build_compare_content_sections(left_car, right_car, compare_decision)
    compare_faq = build_compare_faq(left_car, right_car, compare_decision)
    race_video = build_compare_race_link(left_car, right_car)
    canonical_url = f"{get_base_url()}/compare/{resolved['canonical_slug']}"
    seo_override = get_compare_seo_override(left_car, right_car)
    meta_title = f"{compare_page_title} | CarQuantix"
    meta_description = seo_override.get("meta_description") or build_compare_meta_description(left_car, right_car)
    is_indexable = resolved["canonical_slug"] in build_indexable_compare_slugs(cars, slug_map)
    current_compare_href = f"/compare/{resolved['canonical_slug']}"
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
    if compare_faq:
        page_schema["mainEntity"].setdefault("itemListElement", page_schema["mainEntity"].get("itemListElement", []))
        page_schema["hasPart"] = {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                }
                for item in compare_faq
            ],
        }
    return render_template(
        "compare_detail.html",
        user=user,
        left_car=left_car,
        right_car=right_car,
        compare_rows=compare_rows,
        compare_intro=compare_intro,
        compare_decision=compare_decision,
        compare_page_title=compare_page_title,
        compare_quick_verdict=compare_quick_verdict,
        compare_sections=compare_sections,
        compare_faq=compare_faq,
        race_video=race_video,
        comments_page=f"compare:{resolved['canonical_slug']}",
        canonical_url=canonical_url,
        meta_title=meta_title,
        meta_description=meta_description,
        robots_directive="index,follow",
        adsense_enabled=is_indexable,
        page_schema=page_schema,
        related_car_links=unique_link_entries(
            build_related_car_links(left_car, cars, limit=5) + build_related_car_links(right_car, cars, limit=5),
            limit=8,
        ),
        related_compare_links=build_related_compare_links_for_pair(
            left_car,
            right_car,
            cars,
            slug_map,
            limit=8,
            exclude_href=current_compare_href,
        ),
        related_article_links=build_related_article_links(limit=6),
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
        f"{base_url}/methodology",
        f"{base_url}/about-us",
        f"{base_url}/contact",
        f"{base_url}/sell-car",
        f"{base_url}/pricing",
        f"{base_url}/terms",
        f"{base_url}/refund-policy",
        f"{base_url}/privacy-policy",
    ]
    urls.extend(f"{base_url}/guides/{item['slug']}" for item in GUIDE_ITEMS if item.get("slug"))
    urls.extend(f"{base_url}/blog/{item['slug']}" for item in BLOG_ITEMS if item.get("slug"))
    car_links = build_car_links(cars)
    urls.extend(f"{base_url}/cars/{entry['slug']}" for entry in car_links if entry.get("slug"))
    urls.extend(f"{base_url}{entry['href']}" for entry in build_featured_compare_links(cars, slug_map, limit=None))
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
            meta_description="Compare horsepower, acceleration, top speed, engine details and vehicle performance data with CarQuantix before building your shortlist.",
            robots_directive="index,follow",
            adsense_enabled=False,
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
