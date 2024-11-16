from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.rabbitmq import publish_message

router = APIRouter()

class Item(BaseModel):
    id: int
    name: str
    description: str = None

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        message = item.json()
        publish_message(message)
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))