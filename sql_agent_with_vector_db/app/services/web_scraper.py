import requests
from bs4 import BeautifulSoup
from  app.services.chat_inference import sqlagent
from app.validators.schema.chat_inference import InferenceRequest
from app.validators.schema.web_scraper import ScraperData

class Scraper:
    def scrape_data(self, data: ScraperData):
        # Fetch the content of the URL
        response = requests.get(data.url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from elements
        all_text = soup.get_text(separator=' ', strip=True)

        scraper_data = InferenceRequest(
            query=data.query,
            department=data.department,
            customer_id=data.customer_id,
            updated=data.updated,
            url=data.url,
            web_data=all_text
        )

        response = sqlagent.process_inference(scraper_data)

        return response

# Create an instance of the Scraper
scraper = Scraper()
