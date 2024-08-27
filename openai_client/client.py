import httpx
from config import OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_MODEL
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

    async def generate_content(self, data:str, trends = None):
        """Generování obsahu pomocí Azure OpenAI API."""
        try:          
            #trending_topics = ', '.join(trends)
            payload = {
                "messages": [
                    {"role": "system", "content": (
                        "Jste zkušený redaktor s hlubokými znalostmi v oblasti AI a IT technologií. "
                        "Vaším úkolem je vytvořit detailní, informativní a čtivý článek na základě "
                        "poskytnulého názvu oboru. Článek by měl být strukturovaný, profesionální a vhodný "
                        "pro publikaci na odborném webu. Použijte formátování vhodné pro webový článek, "
                        "včetně titulků, podnadpisů, odstavců a seznamů, pokud je to vhodné. "
                        "Buď velice podrobný a vždu uvěď co nejkonkrétnější příklad."
                        "Zaměřte se na přesnost a přínosnost informací a udržuj přátelský, ale odborný tón."
                        "Hlavním zaměřením je vytvořit use cases, jak v daném oboru využít AI a to havně se zaměřením na LLM."
                        "Výstup piš vždy v češtině a namísto markdownu používej html tagy bez css stylů."
                    )},
                    {"role": "user", "content": f"Na základě následujících dat vytvořte článek: {data}"}
                ]
            }

            timeout = 30.0  # Nastavení timeoutu na 30 sekund

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

