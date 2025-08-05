from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta
from utils import generate_shortcode
from storage import db, url_table
import shortuuid

router = APIRouter()

class URLRequest(BaseModel):
    url: HttpUrl
    validity: int = 30
    shortcode: str | None = None

@router.post("/", status_code=201)
def create_short_url(data: URLRequest, request: Request):
    shortcode = data.shortcode or generate_shortcode()
    now = datetime.utcnow()
    expiry = now + timedelta(minutes=data.validity)

    if db.get(shortcode):
        raise HTTPException(status_code=400, detail="Shortcode already exists")

    entry = {
        "url": data.url,
        "created_at": now.isoformat(),
        "expiry": expiry.isoformat(),
        "hits": 0,
        "clicks": []
    }

    db[shortcode] = entry

    return {
        "shortLink": f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/shorturls/{shortcode}",
        "expiry": expiry.isoformat()
    }

@router.get("/{shortcode}")
def get_stats(shortcode: str):
    entry = db.get(shortcode)

    if not entry:
        raise HTTPException(status_code=404, detail="Shortcode not found")

    return {
        "originalURL": entry["url"],
        "createdAt": entry["created_at"],
        "expiry": entry["expiry"],
        "clicks": entry["clicks"],
        "totalClicks": entry["hits"]
    }
