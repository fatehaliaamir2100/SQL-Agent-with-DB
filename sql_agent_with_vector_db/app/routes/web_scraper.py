from fastapi import APIRouter
from app.validators.schema.data_ingestion import IngestionData
from app.services.web_scraper import scraper
from app.validators.schema.web_scraper import ScraperData

router = APIRouter()

@router.post("/web_scraper")
async def web_scraper(data: ScraperData):
    result = scraper.scrape_data(data)
    return result