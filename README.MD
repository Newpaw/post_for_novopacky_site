
# Web Scraper and Content Generator

This project is a service that performs daily web scraping on specified websites, analyzes the collected data, generates high-quality articles using Azure OpenAI API, and publishes the generated content on a WordPress site.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/newpaw/post_for_novopacky_site.git
   cd post_for_novopacky_site
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment:**

   Create/Update the `config.py` file with your Azure OpenAI API key, endpoint, and WordPress credentials.
```bash
SCRAPING_URLS = [
"xxx",
"xxx",]


OPENAI_API_KEY = "xxx"
OPENAI_ENDPOINT = "xxx"
OPENAI_MODEL = "xxx"

WORDPRESS_BASE_URL = "xxx"
WORDPRESS_USERNAME = "xxx"
WORDPRESS_APPLICATION_PASSWORD = "xxx"
```
## Usage

Run the service:

```bash
python main.py
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.
```