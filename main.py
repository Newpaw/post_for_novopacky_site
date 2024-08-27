import asyncio
#from scraping.scraper import WebScraper
from openai_client.client import AzureOpenAIClient
from wordpress.client import WordpressClient
from utils.logger import logger  # Import loggeru
from random_fields.one_filed import random_field
from trends.trend import GoogleTrends

async def main():
    # Inicializace klientů a scraperu
    #scraper = WebScraper()
    #trends = GoogleTrends()
    openai_client = AzureOpenAIClient()
    wordpress_client = WordpressClient()

    try:
        #scraped_data = await scraper.scrape_sites()
        #trending_topics = trends.get_trending_searches()
        #logger.info(f"Trends: {trending_topics}")
        ai_response = await openai_client.generate_content(random_field)
        logger.info("AI response created!")
        await wordpress_client.create_post(f"Business cases for {random_field}", ai_response)
        logger.info("Ai post posted!")

    except Exception as e:
        logger.exception(f"Chyba při spouštění služby: {e}")

if __name__ == "__main__":
    asyncio.run(main())
