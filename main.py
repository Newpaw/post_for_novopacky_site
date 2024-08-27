import asyncio
from openai_client.client import AzureOpenAIClient
from wordpress.client import WordpressClient
from utils.logger import logger
from random_fields.one_filed import random_field
from database.database import DatabaseClient  # Import DatabaseClient

async def main():
    # Inicializace klientů
    openai_client = AzureOpenAIClient()
    wordpress_client = WordpressClient()
    db_client = DatabaseClient()  # Inicializace DatabaseClient

    try:
        # Generování nového tématu
        topic = await openai_client.generate_topic()

        # Kontrola, zda téma již existuje
        if db_client.topic_exists(topic):
            logger.info(f"Téma '{topic}' již existuje v databázi, nový článek nebude vytvořen.")
            return

        # Uložení nového tématu do databáze
        db_client.save_topic(topic)

        # Generování obsahu na základě nového tématu
        ai_response = await openai_client.generate_content(topic)
        logger.info("AI response created!")

        # Publikování příspěvku na WordPress
        await wordpress_client.create_post(f"{topic}", ai_response)
        logger.info("AI post posted!")

    except Exception as e:
        logger.exception(f"Chyba při spouštění služby: {e}")

if __name__ == "__main__":
    asyncio.run(main())
