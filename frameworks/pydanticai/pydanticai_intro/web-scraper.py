from __future__ import annotations as _annotations

from dataclasses import dataclass
from typing import Any
from httpx import AsyncClient
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext

import asyncio
import os
import logfire

logfire.configure()

app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

class Keypoint(BaseModel):
    keypoint: str

class ScrapedContent(BaseModel):
    content: str
    keypoints: list[Keypoint]

@dataclass
class Deps:
    firecrawl_api_key: str | None


web_scraper_agent = Agent(
    'openai:gpt-4o',
    system_prompt='Scrape the website and return the most relevant information.',
    deps_type=Deps,
    retries=2,
    result_type=ScrapedContent
)


@web_scraper_agent.tool
async def scrape_website(
    ctx: RunContext[Deps], url: str
) -> dict[str, float]:
    """Scrape the website and return the most relevant information.

    Args:
        ctx: The context.
        url: The url of the website to scrape.
    """

    with logfire.span('calling firecrawl API', params={'url': url}) as span:
        result = app.scrape_url(url, params={'formats': ['markdown', 'html']})
        data = result
        span.set_attribute('response', data)

    if data:
        return {'content': data}
    else:
        raise ModelRetry('Could not scrape the website')


async def main():
    firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
    deps = Deps(
        firecrawl_api_key=firecrawl_api_key
    )
    result = await web_scraper_agent.run(
        'Can you give me a summary and keypoints of this website: https://firecrawl.dev', deps=deps
    )
    print('Response:', result.data)


if __name__ == '__main__':
    asyncio.run(main())