# main.py
import json
from typing import Any

from car.models import Car
from car.serializers import CarSerializer


def serialize_car_object(car: Car) -> str:
    """
    Приймає об'єкт Car і повертає JSON-рядок з його даними.
    """
    data = CarSerializer(car).data  # dict
    return json.dumps(data)


def deserialize_car_object(payload: str) -> Car:
    """
    Приймає JSON-рядок і повертає створений/валідований екземпляр Car.
    Кидає rest_framework.exceptions.ValidationError при невалідних даних.
    """
    data: Any = json.loads(payload)
    serializer = CarSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    car: Car = serializer.save()
    return car
