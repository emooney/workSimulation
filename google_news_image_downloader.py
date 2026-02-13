#!/usr/bin/env python3
"""Download the image from the 3rd Google News article to ~/Downloads.

Target runtime: Python 3.14+
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_OUTPUT = Path.home() / "Downloads"


def load_playwright_modules():
    try:
        from playwright.sync_api import TimeoutError as playwright_timeout_error
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Playwright is not installed. Install dependencies with `python3 -m pip install -r requirements.txt` "
            "and then install the browser with `python3 -m playwright install chromium`."
        ) from error

    return sync_playwright, playwright_timeout_error


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return safe.strip("._") or "google_news_article_image"


def extension_from_url(url: str) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else ".jpg"


def fetch_third_article_image_url(timeout_ms: int) -> tuple[str, str]:
    sync_playwright, playwright_timeout_error = load_playwright_modules()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://news.google.com", wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_selector("article", timeout=timeout_ms)

            articles = page.locator("article")
            if articles.count() < 3:
                raise RuntimeError("Google News did not return at least 3 articles.")

            third_article = articles.nth(2)
            image = third_article.locator("img").first
            if image.count() == 0:
                raise RuntimeError("The 3rd article does not contain an image element.")

            image_url = image.get_attribute("src") or image.get_attribute("data-src")
            if not image_url:
                raise RuntimeError("Could not extract an image URL from the 3rd article.")

            if image_url.startswith("//"):
                image_url = f"https:{image_url}"
            elif image_url.startswith("/"):
                image_url = f"https://news.google.com{image_url}"

            headline = third_article.inner_text(timeout=timeout_ms).splitlines()[0]
            return image_url, sanitize_filename(headline)
        except playwright_timeout_error as error:
            raise RuntimeError("Timed out while loading Google News.") from error
        finally:
            browser.close()


def download_image(url: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(request) as response, target_path.open("wb") as output_file:
        output_file.write(response.read())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the image from the 3rd Google News article."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Directory for downloaded image (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=30000,
        help="Playwright navigation timeout in milliseconds (default: 30000)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        image_url, title_slug = fetch_third_article_image_url(timeout_ms=args.timeout_ms)
        image_path = args.output_dir / f"{title_slug}{extension_from_url(image_url)}"
        download_image(image_url, image_path)
    except Exception as error:  # noqa: BLE001
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Saved image to: {image_path}")
    print(f"Source URL: {image_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
