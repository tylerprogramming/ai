from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any

import logfire
from httpx import AsyncClient
from firecrawl import FirecrawlApp
from pydantic import BaseModel

app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

from pydantic_ai import Agent, ModelRetry, RunContext

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')

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
    async with AsyncClient() as client:
        firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        deps = Deps(
            firecrawl_api_key=firecrawl_api_key
        )
        result = await web_scraper_agent.run(
            'https://firecrawl.dev', deps=deps
        )
        print('Response:', result.data)


if __name__ == '__main__':
    asyncio.run(main())