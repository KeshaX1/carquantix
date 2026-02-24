from flask import Flask, redirect, url_for, session, request, render_template, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import json
import hashlib
import urllib.parse
import time
import secrets
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from car_data import load_cars

# Load .env explicitly so it works even if the app is started from another directory
DOTENV_PATH = Path(__file__).with_name(".env")
load_dotenv(DOTENV_PATH, override=True)  # override any stale env values

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")

oauth = OAuth(app)
# GOOGLE DISCOVERY URL (compulsory)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# GOOGLE OAUTH CONFIG
# Fail fast if env variables are missing so we don't hit Google with empty client_id
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise RuntimeError("GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET are not set in environment.")

FACEBOOK_CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID", "")
FACEBOOK_CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET", "")

print(f"[init] .env path={DOTENV_PATH} exists={DOTENV_PATH.exists()}")
print(f"[init] GOOGLE_CLIENT_ID full={GOOGLE_CLIENT_ID}")
if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
    print("[init] Facebook client_id detected")
else:
    print("[init] Facebook client_id/secret not set; Facebook login disabled")

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

USERS_PATH = Path(__file__).with_name("users.json")
PENDING_PATH = Path(__file__).with_name("pending_verifications.json")
PENDING_RESET_PATH = Path(__file__).with_name("pending_resets.json")
PENDING_EXPIRY_SECONDS = 600  # 10 minutes
LOGIN_MEDIA_DIR = Path(__file__).with_name("login logo")
STATIC_DIR = Path(__file__).with_name("static")
SITEMAP_PATH = STATIC_DIR / "sitemap.xml"

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
    "audi-rs6-vs-bmw-m5-cs",
    "bugatti-chiron-vs-koenigsegg-agera-rs",
    "lamborghini-veneno-vs-ferrari-enzo-ferrari",
    "mercedes-benz-sls-vs-aston-martin-lagonda",
    "pagani-huayra-vs-mclaren-720s",
}


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


def session_user_payload(user_dict):
    name = user_dict.get("name") or user_dict.get("email")
    picture = user_dict.get("picture") or letter_avatar(name[:1] if name else "U")
    return {"name": name, "email": user_dict.get("email"), "picture": picture}

@app.route("/login-media/<path:filename>")
def login_media(filename):
    return send_from_directory(LOGIN_MEDIA_DIR, filename)

@app.route("/health")
def health():
    return jsonify({"ok": True}), 200

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/about-us")
def about_us():
    return render_template("about_us.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/cars/<slug>")
def car_detail(slug):
    _, slug_map = load_cars()
    car = slug_map.get(slug)
    if not car:
        return "Not Found", 404
    specs = build_car_specs(car)
    meta_title = f"{car.get('name', 'Car')} | CarQuantix"
    meta_description = build_car_meta_description(car)
    return render_template(
        "car_detail.html",
        car=car,
        specs=specs,
        meta_title=meta_title,
        meta_description=meta_description,
        canonical_url=request.base_url,
    )


@app.route("/sitemap.xml")
def sitemap():
    if SITEMAP_PATH.exists():
        return send_from_directory(STATIC_DIR, "sitemap.xml")
    _, slug_map = load_cars()
    base_url = request.host_url.rstrip("/")
    urls = [
        f"{base_url}/",
        f"{base_url}/about-us",
        f"{base_url}/contact",
        f"{base_url}/privacy-policy",
    ]
    urls.extend(f"{base_url}/{slug}" for slug in sorted(SEO_SLUGS))
    urls.extend(f"{base_url}/cars/{slug}" for slug in sorted(slug_map.keys()))
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{entries}</urlset>"
    )
    return app.response_class(xml, mimetype="application/xml")


@app.route("/<slug>")
def seo_slug(slug):
    normalized = re.sub(r"\s+", "-", (slug or "").strip().lower())
    if normalized in SEO_SLUGS:
        if normalized != slug:
            return redirect(f"/{normalized}", code=301)
        user = session.get("user")
        return render_template("index.html", user=user)
    return "Not Found", 404

@app.route("/login/google")
def login_google():
    print(f"[auth] using client_id={GOOGLE_CLIENT_ID}")
    redirect_uri = url_for("authorize_google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route("/auth/callback/google")
def authorize_google():
    token = oauth.google.authorize_access_token()
    user = oauth.google.get("userinfo").json()
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
    session["user"] = session_user_payload(payload)
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
    app.run(debug=True)
