import json
from fastapi import APIRouter
from app.validators.schema.chat_inference import InferenceRequest, InferenceResponse
from app.services.chat_inference import sqlagent 

router = APIRouter()

@router.post("/chat_inference", response_model=dict)
async def chat_inference(request: InferenceRequest):
    print(request)
    result = sqlagent.process_inference(request)
    return json.loads(result["response"])
