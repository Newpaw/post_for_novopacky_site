import httpx
from scraping.parser import parse_html
from config import SCRAPING_URLS
from utils.logger import logger

class WebScraper:
    """Třída pro web scraping."""

    async def scrape_sites(self):
        scraped_data = []

        async with httpx.AsyncClient() as client:
            for url in SCRAPING_URLS:
                logger.debug(f"Scrapping: {url}")

                response = await client.get(url)

                if response.status_code != 200:
                    logger.error(f"Failed to fetch URL: {url}")
                    continue
                data = parse_html(response.text)
                scraped_data.append(data)

        return scraped_data
