from fastapi import APIRouter
from app.validators.schema.data_ingestion import IngestionData
from app.services.data_ingestion import ingestor

router = APIRouter()

@router.post("/data_ingestion")
async def data_ingestion(data: IngestionData):
    result = ingestor.ingest_data(data.data, data.department)
    return result

@router.post("/document_ingestion")
async def data_ingestion(data: IngestionData):
    result = ingestor.ingest_data(data.data, data.department)
    return result
