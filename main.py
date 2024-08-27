import asyncio
from scraping.scraper import WebScraper
from openai_client.client import AzureOpenAIClient
from wordpress.client import WordpressClient
from utils.logger import logger  # Import loggeru

async def main():
    # Inicializace klientů a scraperu
    scraper = WebScraper()
    openai_client = AzureOpenAIClient()
    wordpress_client = WordpressClient()

    try:
        scraped_data = await scraper.scrape_sites()
        ai_response = await openai_client.generate_content(scraped_data)
        await wordpress_client.create_post("Denní aktualizace", ai_response)

    except Exception as e:
        logger.exception(f"Chyba při spouštění služby: {e}")

if __name__ == "__main__":
    asyncio.run(main())
