import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from car_data import load_cars  # noqa: E402
from main import (  # noqa: E402
    BLOG_ITEMS,
    GUIDE_ITEMS,
    build_car_links,
    build_featured_compare_links,
    select_featured_car_links,
)


def generate_sitemap(base_url: str, output_path: Path) -> None:
    cars, slug_map = load_cars()
    urls = [
        f"{base_url}/",
        f"{base_url}/news",
        f"{base_url}/guides",
        f"{base_url}/blog",
        f"{base_url}/methodology",
        f"{base_url}/about-us",
        f"{base_url}/contact",
        f"{base_url}/pricing",
        f"{base_url}/terms",
        f"{base_url}/refund-policy",
        f"{base_url}/privacy-policy",
    ]
    urls.extend(f"{base_url}/guides/{item['slug']}" for item in GUIDE_ITEMS if item.get("slug"))
    urls.extend(f"{base_url}/blog/{item['slug']}" for item in BLOG_ITEMS if item.get("slug"))
    featured_car_links = select_featured_car_links(build_car_links(cars))
    urls.extend(f"{base_url}/cars/{entry['slug']}" for entry in featured_car_links if entry.get("slug"))
    urls.extend(f"{base_url}{entry['href']}" for entry in build_featured_compare_links(cars, slug_map))
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{entries}</urlset>"
    )
    output_path.write_text(xml, encoding="utf-8")


def main() -> None:
    base_url = os.environ.get("BASE_URL", "https://carquantix.com").rstrip("/")
    output_path = PROJECT_ROOT / "static" / "sitemap.xml"
    generate_sitemap(base_url, output_path)
    print(f"Wrote sitemap to {output_path}")


if __name__ == "__main__":
    main()
