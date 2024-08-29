import httpx
from config import BRAVE_API_KEY
from utils.logger import logger

class BraveSearchClient:
    """Class for interacting with the Brave Search API."""

    def __init__(self, api_key: str = BRAVE_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    async def fetch_search_results(self, query: str) -> dict:
        """Fetch search results from Brave API for a given query with country code set to 'cs'."""
        params = {
            "q": query,
            "search_lang": "cs",
            "freshness": "pd"

        }
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }

        async with httpx.AsyncClient() as client:
            logger.debug(f"Fetching search results for query: {query} with country code 'cs'")

            try:
                response = await client.get(self.base_url, headers=headers, params=params)

                if response.status_code != 200:
                    # Log the full response content for debugging purposes
                    logger.error(
                        f"Failed to fetch results for query: {query} with status code {response.status_code}. "
                        f"Response content: {response.text}"
                    )
                    return {}
                
                logger.debug(f"Successfully fetched results for query: {query}")
                return response.json()

            except httpx.RequestError as exc:
                logger.error(f"An error occurred while requesting {exc.request.url}: {exc}")
                return {}

    def extract_titles_and_descriptions(self, search_results: dict) -> dict:
        """Extract titles and descriptions from search results."""
        results_dict = {}

        if "web" in search_results and "results" in search_results["web"]:
            for result in search_results["web"]["results"]:
                title = result.get("title")
                description = result.get("description")
                results_dict[title] = description

        return results_dict
    
