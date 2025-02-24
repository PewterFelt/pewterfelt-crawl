from typing import TypedDict

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from flask import Flask, request


class TagRequest(TypedDict):
    url: str


async def crawl_content(url: str):
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)

        return result.markdown


app = Flask(__name__)


@app.route("/api/crawl", methods=["POST"])
async def crawl():
    data: TagRequest = request.get_json()
    if not data or "url" not in data:
        return {"error": "Missing URL in request body"}, 400  # pyright: ignore[reportUnreachable]

    url = data["url"]

    try:
        content = await crawl_content(url)
    except Exception:
        return {"error": "Failed to crawl URL"}, 500

    return {"content": str(content)}
