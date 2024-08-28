import httpx
from config import (OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_MODEL)
from utils.logger import logger
from database.database import DatabaseClient

class AzureOpenAIClient:
    """Třída pro komunikaci s Azure OpenAI API."""

    def __init__(self, db_path='articles.db'):
        self.api_key = OPENAI_API_KEY
        self.endpoint = OPENAI_ENDPOINT
        self.model = OPENAI_MODEL
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        self.db_client = DatabaseClient(db_path) 

    async def generate_unique_topic(self):
        """Generování unikátního nápadu na téma pomocí Azure OpenAI API."""
        try:
            # Načtení existujících topiců z databáze
            existing_topics = self.get_existing_topics()

            # Vytvoření promptu s existujícími topicy
            existing_topics_str = "; ".join(existing_topics)
            prompt = (
                "Jste zkušený redaktor s hlubokými znalostmi v oblasti AI a IT technologií. "
                "Vaším úkolem je vytvořit nápad na nové téma pro článek zaměřený na telekomunikace nebo kontaktní centra."
                "Věnuj se tomu oborům, které dělají operátoři v České republioce (O2, T-Mobile, Vodafone) jako je telekomunikace, TV, prodej HW (telefonů) a kontaktní centra."
                "a využití AI v tomto oboru. Přemýšlejte o aktuálních trendech a inovacích, které by mohly být zajímavé. "
                "Vyhněte se tématům, které již existují: " + existing_topics_str +
                ". Vrať jako odpověď POUZE hlavní téma!"
            )

            payload = {
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Navrhněte nápad na nové téma článku zaměřeného na telekomunikace a AI."}
                ]
            }
            timeout = 60.0

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=self.headers,
                    json=payload
                )

            response.raise_for_status()
            result = response.json()
            new_topic = result["choices"][0]["message"]["content"]

            # Ověření, zda nové téma již neexistuje v databázi
            if self.db_client.topic_exists(new_topic):
                logger.warning(f"Téma '{new_topic}' již existuje v databázi.")
                return None

            # Uložení nového tématu do databáze
            self.db_client.save_topic(new_topic)
            logger.info(f"Nové téma '{new_topic}' bylo úspěšně vygenerováno a uloženo.")
            return new_topic

        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise

        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}")
            raise

        except Exception as exc:
            logger.exception(f"Unexpected error occurred: {exc}")
            raise

    def get_existing_topics(self):
        """Načte všechny existující topicy z databáze."""
        cursor = self.db_client.conn.cursor()
        cursor.execute('SELECT topic FROM articles')
        topics = cursor.fetchall()
        logger.debug(f"Existující topicy: {topics}")
        return [topic[0] for topic in topics]


    async def generate_content(self, topic: str):
        """Generování obsahu na základě zadaného tématu pomocí Azure OpenAI API."""
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": (
                        "Jste zkušený redaktor s hlubokými znalostmi v oblasti AI a IT technologií. "
                        "Vaším úkolem je vytvořit detailní, informativní a čtivý článek na základě "
                        "zadaného tématu. Článek by měl být strukturovaný, profesionální a vhodný "
                        "pro publikaci na odborném webu. Použijte formátování vhodné pro webový článek, "
                        "včetně titulků, podnadpisů, odstavců a seznamů, pokud je to vhodné. "
                        "Buď velice podrobný a vždy uváděj co nejkonkrétnější příklad."
                        "Zaměřte se na přesnost a přínosnost informací a udržuj přátelský, ale odborný tón."
                        "Výstup piš vždy v češtině a namísto markdownu používej html tagy bez css stylů."
                    )},
                    {"role": "user", "content": f"Vytvořte článek na téma: {topic}"}
                ]
            }
            timeout = 60.0
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=self.headers,
                    json=payload
                )

            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise

        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}")
            raise

        except Exception as exc:
            logger.exception(f"Unexpected error occurred: {exc}")
            raise


