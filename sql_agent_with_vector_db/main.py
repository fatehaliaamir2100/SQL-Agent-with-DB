from fastapi import FastAPI
from app.routes import data_ingestion, chat_inference, web_scraper

app = FastAPI()

app.include_router(data_ingestion.router)
app.include_router(chat_inference.router)
app.include_router(web_scraper.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
