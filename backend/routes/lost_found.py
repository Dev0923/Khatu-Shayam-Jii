from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.sql_models import LostItem, FoundItem, LostPerson, User
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/lost-found", tags=["Lost & Found"])

# Pydantic models for incoming data
class LostItemCreate(BaseModel):
    category: str
    date_lost: datetime
    location: str
    description: Optional[str] = None
    contact_name: str
    contact_phone: str
    photo_url: Optional[str] = None
    user_id: Optional[int] = None

class FoundItemCreate(BaseModel):
    category: str
    date_found: datetime
    location_found: str
    storage_location: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None

class LostPersonCreate(BaseModel):
    name: str
    age: int
    gender: Optional[str] = None
    clothes_description: Optional[str] = None
    last_seen_location: str
    last_seen_time: datetime
    contact_name: str
    contact_phone: str
    photo_url: Optional[str] = None

@router.post("/lost-item", status_code=status.HTTP_201_CREATED)
async def create_lost_item(item: LostItemCreate, db: Session = Depends(get_db)):
    db_item = LostItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.post("/found-item", status_code=status.HTTP_201_CREATED)
async def create_found_item(item: FoundItemCreate, db: Session = Depends(get_db)):
    # In a real app, verify admin here
    db_item = FoundItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.post("/lost-person", status_code=status.HTTP_201_CREATED)
async def create_lost_person(person: LostPersonCreate, db: Session = Depends(get_db)):
    db_person = LostPerson(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.get("/found-items")
async def get_found_items(db: Session = Depends(get_db)):
    items = db.query(FoundItem).filter(FoundItem.status == "In Storage").all()
    return items

@router.put("/claim/{id}")
async def claim_found_item(id: int, claim_id: str, db: Session = Depends(get_db)):
    item = db.query(FoundItem).filter(FoundItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.status = "Claimed"
    item.claim_id = claim_id
    db.commit()
    return {"message": "Item claimed successfully"}

@router.get("/admin/items")
async def get_all_items(db: Session = Depends(get_db)):
    lost_items = db.query(LostItem).all()
    found_items = db.query(FoundItem).all()
    lost_persons = db.query(LostPerson).all()
    return {
        "lost_items": lost_items,
        "found_items": found_items,
        "lost_persons": lost_persons
    }

@router.post("/notify/{lost_item_id}")
async def notify_user(lost_item_id: int, db: Session = Depends(get_db)):
    item = db.query(LostItem).filter(LostItem.id == lost_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    
    # Stub notification logic
    # In reality, we'd use Twilio/Gupshup etc to send SMS/WhatsApp to item.contact_phone
    print(f"Simulating notification sent to {item.contact_phone} for item {item.category}")
    
    item.status = "Found"
    db.commit()
    
    return {"message": f"Notification sent to {item.contact_phone}"}
