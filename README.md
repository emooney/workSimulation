# workSimulation

## Google News opener (Python 3.14 + Playwright + Chrome)

This repo includes `google_news_open_chrome.py`, a Python app that opens:

- `https://news.google.com`
- using Playwright
- with **Google Chrome** (`channel="chrome"`)

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chrome
```

## Run

```bash
python3 google_news_open_chrome.py
```

Optional:

```bash
python3 google_news_open_chrome.py --headless --wait-seconds 3
```
