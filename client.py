import httpx
import asyncio
from utils.logger import logger
from httpx import BasicAuth
from typing import Protocol


class HttpClient(Protocol):
    """Interface for HTTP client."""

    async def post(self, url: str, auth: BasicAuth, json: dict) -> httpx.Response:
        """Send a POST request."""
        ...


class AsyncHttpClient:
    """Concrete implementation of an asynchronous HTTP client using httpx."""

    async def post(self, url: str, auth: BasicAuth, json: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, auth=auth, json=json)
        return response


class WordpressClient:
    """Client to interact with WordPress REST API."""

    def __init__(self, base_url: str, username: str, application_password: str, http_client: HttpClient):
        self.base_url = base_url
        self.auth = BasicAuth(username, application_password)
        self.http_client = http_client

    async def create_post(self, title: str, content: str, status: str = "publish") -> None:
        """Create a new post in WordPress."""
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        data = {
            "title": title,
            "content": content,
            "status": status
        }
        response = await self.http_client.post(url, auth=self.auth, json=data)
        self._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> None:
        """Handle the response from the server."""
        if response.status_code == 201:
            logger.info("Příspěvek byl úspěšně vytvořen.")
        else:
            logger.error(f"Chyba: {response.status_code}")
            logger.debug(response.json())


async def main():
    """Main function to run the WordPress client."""
    # Konfigurace
    base_url = "https://novopacky.com"
    username = "newpaw"  # Nahraďte vaším uživatelským jménem
    application_password = "rXF2 S4s6 bHld 3zXB ItlE XPsZ"  # Vaše heslo aplikace

    # Vytvoření klienta
    http_client = AsyncHttpClient()
    wordpress_client = WordpressClient(base_url, username, application_password, http_client)

    # Vytvoření příspěvku
    await wordpress_client.create_post("Titul nového příspěvku", "Obsah nového příspěvku.")


if __name__ == "__main__":
    asyncio.run(main())
