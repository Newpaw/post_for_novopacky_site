import httpx
from config import ( OPENAI_API_KEY, 
                    OPENAI_ENDPOINT, OPENAI_MODEL)
from utils.logger import logger

class AzureOpenAIClient:
    """Třída pro komunikaci s Azure OpenAI API."""

    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.endpoint = OPENAI_ENDPOINT
        self.model = OPENAI_MODEL
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

    async def generate_topic(self):
        """Generování nápadu na téma pomocí Azure OpenAI API."""
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": (
                        "Jste zkušený redaktor s hlubokými znalostmi v oblasti AI a IT technologií. "
                        "Vaším úkolem je vytvořit nápad na nové téma pro článek zaměřený na telekomunikace "
                        "a využití AI v tomto oboru. Přemýšlejte o aktuálních trendech a inovacích, které by mohly být zajímavé."
                        "Vrať jako odpověď POUZE hlavní téma!"
                    )},
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


