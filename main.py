from flask import Flask, redirect, url_for, session, request, render_template, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import json
import hashlib
import hmac
import urllib.parse
import time
import secrets
import smtplib
import requests
from datetime import datetime
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from car_data import load_cars

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

def resolve_data_path(env_var_name, filename):
    explicit = (os.environ.get(env_var_name, "") or "").strip()
    if explicit:
        return Path(explicit).expanduser()
    data_dir = (os.environ.get("APP_DATA_DIR", "") or "").strip()
    if data_dir:
        return Path(data_dir).expanduser() / filename
    return Path(__file__).with_name(filename)


def ensure_parent_dir(path_obj):
    path_obj.parent.mkdir(parents=True, exist_ok=True)


USERS_PATH = resolve_data_path("USERS_PATH", "users.json")
PENDING_PATH = resolve_data_path("PENDING_PATH", "pending_verifications.json")
PENDING_RESET_PATH = resolve_data_path("PENDING_RESET_PATH", "pending_resets.json")
PENDING_EXPIRY_SECONDS = 600  # 10 minutes
LOGIN_MEDIA_DIR = Path(__file__).with_name("login logo")
STATIC_DIR = Path(__file__).with_name("static")
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
FEATURED_COMPARE_REFERENCES = [
    ("RS6", "M5 CS"),
    ("Chiron", "Agera RS"),
    ("Veneno", "Enzo Ferrari"),
    ("SLS", "Lagonda"),
    ("Huayra", "720S"),
    ("M3", "RS3"),
]
FEATURED_COMPARE_LIMIT = int(os.environ.get("FEATURED_COMPARE_LIMIT", "12"))
LEGACY_COMPARE_SLUGS = {
    "audi-rs6-vs-bmw-m5-cs": ("RS6", "M5 CS"),
    "bugatti-chiron-vs-koenigsegg-agera-rs": ("Chiron", "Agera RS"),
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


def is_local_host(host):
    host_only = (host or "").split(":")[0].lower()
    return host_only in {"127.0.0.1", "localhost", "::1"}


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
        specs.append({"label": "Price", "value": price})
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
        {
            "label": "Price",
            "left_value": car_a.get("price") or "-",
            "right_value": car_b.get("price") or "-",
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


def upsert_user(email, patch):
    email = (email or "").strip().lower()
    if not email:
        return None
    updates = patch or {}
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
        meta_title="CarQuantix - Best Cars by HP, Acceleration, Top Speed and Cost",
        meta_description="Compare car and motorcycle horsepower, acceleration and top speed. Find the best performance value with CarQuantix.",
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

    users = load_users()
    idx = find_user_index(users, ids["email"])
    if idx is None:
        idx = find_user_index_by_billing_ids(users, ids["customer_id"], ids["subscription_id"])

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

    if idx is None:
        if not ids["email"]:
            return jsonify({"ok": True, "message": "No matching user for webhook payload."}), 200
        new_user = {"name": ids["email"], "email": ids["email"], "subscription_status": "free"}
        for key, value in patch.items():
            if value is not None:
                new_user[key] = value
        users.append(new_user)
        save_users(users)
        return jsonify({"ok": True, "updated": ids["email"]}), 200

    changed = False
    for key, value in patch.items():
        if value is None:
            continue
        if users[idx].get(key) != value:
            users[idx][key] = value
            changed = True
    if changed:
        save_users(users)
    return jsonify({"ok": True, "updated": users[idx].get("email")}), 200


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
    users = load_users()
    users.append(user_record)
    save_users(users)

    pending.pop(email, None)
    save_pending(pending)

    session["user"] = session_user_payload(user_record)
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

    users = load_users()
    updated_user = None
    for idx, u in enumerate(users):
        if u.get("email", "").lower() == email:
            users[idx]["password_hash"] = generate_password_hash(new_password)
            updated_user = users[idx]
            break
    if not updated_user:
        pending.pop(email, None)
        save_reset_pending(pending)
        return jsonify({"ok": False, "message": "No account found for this email."}), 400

    save_users(users)
    pending.pop(email, None)
    save_reset_pending(pending)

    session["user"] = session_user_payload(updated_user)
    return jsonify({"ok": True, "message": "Password updated. You are now logged in."})


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    # Render (and most PaaS) provide the port via $PORT and require binding to 0.0.0.0
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
