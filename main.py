# main.py
import json
from typing import Union

from car.models import Car
from car.serializers import CarSerializer


def serialize_car_object(car: Car) -> bytes:
    """
    Приймає Car і повертає JSON як bytes без
    зайвих пробілів.
    Має включати поле id.
    """
    data = CarSerializer(car).data
    return json.dumps(data,
                      separators=(",", ":")).encode("utf-8")


def deserialize_car_object(payload: Union[str, bytes]) -> Car:
    """
    Приймає JSON (str або bytes) і повертає
    створений екземпляр Car.
    """
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    data = json.loads(payload)
    ser = CarSerializer(data=data)
    ser.is_valid(raise_exception=True)
    return ser.save()
