from __future__ import annotations as _annotations

from dataclasses import dataclass
from firecrawl import Firecrawl
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext

import asyncio
import os
import logfire

logfire.configure(send_to_logfire='if-token-present')  # runs without a Logfire token too

app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

class Keypoint(BaseModel):
    keypoint: str

class ScrapedContent(BaseModel):
    content: str
    keypoints: list[Keypoint]

@dataclass
class Deps:
    firecrawl_api_key: str | None


web_scraper_agent = Agent(
    'openai:gpt-5.4-mini',
    system_prompt='Scrape the website and return the most relevant information.',
    deps_type=Deps,
    retries=2,
    output_type=ScrapedContent
)


@web_scraper_agent.tool
async def scrape_website(
    ctx: RunContext[Deps], url: str
) -> dict[str, str]:
    """Scrape the website and return the most relevant information.

    Args:
        ctx: The context.
        url: The url of the website to scrape.
    """

    with logfire.span('calling firecrawl API', params={'url': url}) as span:
        result = app.scrape(url, formats=['markdown'])
        data = result.markdown
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
    print('Response:', result.output)


if __name__ == '__main__':
    asyncio.run(main())