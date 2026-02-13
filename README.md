# workSimulation

## Google News opener (Python 3.14 + Playwright)

This repo includes `google_news_open.py`, a Python app that opens:

- `https://news.google.com`
- using Playwright

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

## Run

```bash
python3 google_news_open.py
```

Optional:

```bash
python3 google_news_open.py --wait-seconds 3
```
