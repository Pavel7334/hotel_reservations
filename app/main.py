from fastapi import FastAPI, Query
from datetime import date
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5),
):
    print(date_to, date_from, has_spa, stars)
    return date_from, date_to


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
def add_booking(booking: SBooking):
    pass
