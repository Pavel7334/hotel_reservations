from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic.v1 import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
async def add_booking(
    booking: SNewBooking,
    background_tasks: BackgroundTasks,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = parse_obj_as(SNewBooking, booking).model_dump()
    # Celery - отдельная библиотека
    # send_booking_confirmation_email.delay(booking, user.email)
    # Background Tasks - встроено в FastAPI
    # background_tasks.add_task(send_booking_confirmation_email, booking, user.email)
    return booking


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)



