import httpx
from httpx import BasicAuth
from config import WORDPRESS_BASE_URL, WORDPRESS_USERNAME, WORDPRESS_APPLICATION_PASSWORD
from utils.logger import logger


class WordpressClient:
    """Třída pro publikování na WordPress."""

    def __init__(self):
        self.base_url = WORDPRESS_BASE_URL
        self.auth = BasicAuth(WORDPRESS_USERNAME,
                              WORDPRESS_APPLICATION_PASSWORD)

    async def create_post(self, title: str, content: str):
        """Vytvoření nového příspěvku na WordPress stránce."""
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        data = {
            "title": title,
            "content": content,
            "status": "publish"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, auth=self.auth, json=data)

            if response.status_code == 201:
                logger.debug("Příspěvek byl úspěšně vytvořen.")
            else:
                logger.error(f"Chyba: {response.status_code}")
                logger.debug(response.json())
