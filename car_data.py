from pathlib import Path
import json
import re
import unicodedata

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


def _parse_js_array(array_text: str):
    cleaned = re.sub(r"//.*", "", array_text)
    cleaned = re.sub(r"([A-Za-z0-9_]+)\s*:", r'"\1":', cleaned)
    cleaned = cleaned.replace("'", '"')
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


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

    _CAR_CACHE, _CAR_SLUG_MAP = cars, slug_map
    return _CAR_CACHE, _CAR_SLUG_MAP
