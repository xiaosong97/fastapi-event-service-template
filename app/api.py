from datetime import tzinfo, timezone
from zoneinfo import ZoneInfo
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.schemas import EventIn, EventOut
from app.models import Event


router = APIRouter()

LOCAL_TZ = ZoneInfo("Asia/Shanghai")

def to_local(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(LOCAL_TZ)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events", response_model=EventOut)
def create_event(event: EventIn, db: Session = Depends(get_db)):
    obj = Event(type=event.type, payload=json.dumps(event.payload))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {
        "id": obj.id,
        "type": obj.type,
        "payload": event.payload,
        "created_at": to_local(obj.created_at),
    }


@router.get("/events", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    items = db.query(Event).order_by(Event.id.desc()).all()
    return [
        {
            "id": e.id,
            "type": e.type,
            "payload": json.loads(e.payload),
            "created_at": to_local(e.created_at),
        }
        for e in items
    ]
