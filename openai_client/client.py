import httpx
from config import OPENAI_API_KEY, OPENAI_ENDPOINT, OPENAI_MODEL


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

    async def generate_content(self, data):
        """Generování obsahu pomocí Azure OpenAI API."""
        payload = {
            "messages": [
                {"role": "system", "content": (
                    "Jste zkušený redaktor s hlubokými znalostmi v oblasti AI a IT technologií. "
                    "Vaším úkolem je vytvořit detailní, informativní a čtivý článek na základě "
                    "poskytnutých dat. Článek by měl být strukturovaný, profesionální a vhodný "
                    "pro publikaci na odborném webu. Použijte formátování vhodné pro webový článek, "
                    "včetně titulků, podnadpisů, odstavců a seznamů, pokud je to vhodné. "
                    "Zaměřte se na přesnost a přínosnost informací a udržuj přátelský, ale odborný tón."
                    "Výstup piš vždy v češtině a namísto markdownu používej html tagy."
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
