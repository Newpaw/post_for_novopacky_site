import asyncio
from openai_client.client import AzureOpenAIClient
from wordpress.client import WordpressClient
from utils.logger import logger

async def main():
    # Inicializace klientů
    openai_client = AzureOpenAIClient()
    wordpress_client = WordpressClient()

    try:
        # Generování nového unikátního tématu
        topic = await openai_client.generate_unique_topic()

        # Kontrola, zda bylo úspěšně vygenerováno nové téma
        if topic is None:
            logger.info("Nové unikátní téma se nepodařilo vygenerovat, ukončuji proces.")
            return

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
