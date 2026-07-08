from pathlib import Path
import json
import re
import unicodedata
import urllib.parse

STATIC_DIR = Path(__file__).with_name("static")
VEHICLES_JS_PATH = STATIC_DIR / "script.js"

_CAR_CACHE = None
_CAR_SLUG_MAP = None


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only.lower()).strip("-")
    return slug or "car"


def _extract_array(text: str, var_name: str):
    marker = f"const {var_name} = ["
    start = text.find(marker)
    if start == -1:
        return None
    start = text.find("[", start)
    depth = 0
    in_string = None
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
        else:
            if ch in ("'", '"'):
                in_string = ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    return None


def _strip_js_line_comments(text: str) -> str:
    output = []
    in_string = None
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        next_ch = text[i + 1] if i + 1 < len(text) else ""
        if in_string:
            output.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_string = ch
            output.append(ch)
            i += 1
            continue
        if ch == "/" and next_ch == "/":
            while i < len(text) and text[i] not in "\r\n":
                i += 1
            continue
        output.append(ch)
        i += 1
    return "".join(output)


def _parse_js_array(array_text: str):
    cleaned = _strip_js_line_comments(array_text)
    cleaned = re.sub(r"([,{]\s*)([A-Za-z0-9_]+)\s*:", r'\1"\2":', cleaned)
    def _replace_single_quoted(match):
        content = match.group(1)
        content = content.replace("\\", "\\\\").replace('"', '\\"')
        return f"\"{content}\""
    cleaned = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", _replace_single_quoted, cleaned)
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    cleaned = re.sub(r"[\x00-\x1F]", " ", cleaned)
    return json.loads(cleaned)


def _placeholder_image(label: str) -> str:
    safe_label = (label or "Vehicle").strip() or "Vehicle"
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/>'
        "</linearGradient></defs>"
        '<rect width="1200" height="675" fill="url(#g)"/>'
        '<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
        'fill="#cbd5e1" font-family="Arial, sans-serif" font-size="56" font-weight="700">'
        f"{safe_label}</text></svg>"
    )
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _normalize_asset_path(path: str, label: str = "Vehicle") -> str:
    if not path:
        return _placeholder_image(label)

    normalized = str(path).replace("\\", "/")
    if normalized.startswith(("http://", "https://", "data:")):
        return normalized

    replacements = (
        ("/static/images/", "/static/images-webp/"),
        ("/static/rearimg/", "/static/rearimg-webp/"),
        ("/static/mimages/", "/static/mimages-webp/"),
        ("/static/mrearimg/", "/static/mrearimg-webp/"),
    )

    for source_prefix, target_prefix in replacements:
        if not normalized.startswith(source_prefix):
            continue
        filename = normalized[len(source_prefix):]
        stem = re.sub(r"\.(jpe?g|png)$", "", filename, flags=re.IGNORECASE)
        candidate = f"{target_prefix}{stem}.webp"
        candidate_fs = STATIC_DIR / candidate.removeprefix("/static/")
        if candidate_fs.exists():
            return candidate
        break

    original_fs = STATIC_DIR / normalized.removeprefix("/static/")
    if original_fs.exists():
        return normalized

    return _placeholder_image(label)


def load_cars():
    global _CAR_CACHE, _CAR_SLUG_MAP
    if _CAR_CACHE is not None:
        return _CAR_CACHE, _CAR_SLUG_MAP

    if not VEHICLES_JS_PATH.exists():
        _CAR_CACHE, _CAR_SLUG_MAP = [], {}
        return _CAR_CACHE, _CAR_SLUG_MAP

    text = VEHICLES_JS_PATH.read_text(encoding="utf-8")
    array_text = _extract_array(text, "VEHICLES")
    if not array_text:
        _CAR_CACHE, _CAR_SLUG_MAP = [], {}
        return _CAR_CACHE, _CAR_SLUG_MAP

    try:
        cars = _parse_js_array(array_text)
    except json.JSONDecodeError:
        _CAR_CACHE, _CAR_SLUG_MAP = [], {}
        return _CAR_CACHE, _CAR_SLUG_MAP

    slug_map = {}
    for car in cars:
        name = car.get("name") or car.get("id") or ""
        car["img"] = _normalize_asset_path(car.get("img"), name)
        if car.get("rearImg"):
            car["rearImg"] = _normalize_asset_path(car.get("rearImg"), f"{name} rear view")
        base_slug = slugify(name)
        slug = base_slug
        if slug in slug_map:
            hint = slugify(car.get("id") or "")
            if hint and hint != base_slug:
                slug = f"{base_slug}-{hint}"
            count = 2
            while slug in slug_map:
                slug = f"{base_slug}-{count}"
                count += 1
        car["slug"] = slug
        slug_map[slug] = car

        year_match = re.match(r"^(\\d{4})-(.+)$", slug)
        if year_match:
            alt_slug = f"{year_match.group(2)}-{year_match.group(1)}"
            if alt_slug not in slug_map:
                slug_map[alt_slug] = car

    _CAR_CACHE, _CAR_SLUG_MAP = cars, slug_map
    return _CAR_CACHE, _CAR_SLUG_MAP
