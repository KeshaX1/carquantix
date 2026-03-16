from pathlib import Path
import os
from pathlib import Path

from car_data import load_cars


def generate_sitemap(base_url: str, output_path: Path) -> None:
    _, slug_map = load_cars()
    urls = [
        f"{base_url}/",
        f"{base_url}/news",
        f"{base_url}/guides",
        f"{base_url}/blog",
        f"{base_url}/about-us",
        f"{base_url}/contact",
        f"{base_url}/privacy-policy",
    ]
    urls.extend(f"{base_url}/cars/{slug}" for slug in sorted(slug_map.keys()))
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{entries}</urlset>"
    )
    output_path.write_text(xml, encoding="utf-8")


def main() -> None:
    base_url = os.environ.get("BASE_URL", "https://carquantix.com").rstrip("/")
    output_path = Path(__file__).resolve().parent.parent / "static" / "sitemap.xml"
    generate_sitemap(base_url, output_path)
    print(f"Wrote sitemap to {output_path}")


if __name__ == "__main__":
    main()
