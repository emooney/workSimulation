# workSimulation

## Google News image downloader (Python 3.14 + Playwright)

This repo now includes `google_news_image_downloader.py`, a small Python app that:

1. Opens `https://news.google.com` with Playwright.
2. Finds the **3rd news article** on the page.
3. Extracts that article's image URL.
4. Downloads the image to your **Downloads** folder (`~/Downloads`, good for Chromebook/Linux environments).

## Setup (Chromebook)

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

## Run

```bash
python3 google_news_image_downloader.py
```

Optional flags:

```bash
python3 google_news_image_downloader.py --output-dir ~/Downloads --timeout-ms 45000
```
