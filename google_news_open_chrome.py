#!/usr/bin/env python3
"""Open news.google.com with Playwright using Google Chrome.

Target runtime: Python 3.14+
"""

from __future__ import annotations

import argparse
import sys


def load_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Playwright is not installed. Run `python3 -m pip install -r requirements.txt` "
            "and then `python3 -m playwright install chrome`."
        ) from error
    return sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open https://news.google.com in Google Chrome via Playwright."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode (default is headed).",
    )
    parser.add_argument(
        "--wait-seconds",
        type=float,
        default=8,
        help="How long to keep the page open before exiting (default: 8).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        sync_playwright = load_playwright()

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=args.headless)
            page = browser.new_page()
            page.goto("https://news.google.com", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(int(args.wait_seconds * 1000))
            print("Opened https://news.google.com using Playwright + Google Chrome.")
            browser.close()
    except Exception as error:  # noqa: BLE001
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
