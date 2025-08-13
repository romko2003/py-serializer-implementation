# car/serializers.py
from typing import Any, Dict

from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)
from rest_framework import serializers

from .models import Car


_hp_field = Car._meta.get_field("horse_powers")
_HP_MIN = next(
    (v.limit_value for v in _hp_field.validators if isinstance(v,
    MinValueValidator)),
    None,
)
_HP_MAX = next(
    (v.limit_value for v in _hp_field.validators if
     isinstance(v, MaxValueValidator)),
    None,
)


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    # важливо: валідатори меж прямо в полі серіалізатора
    horse_powers = serializers.IntegerField(
        min_value=_HP_MIN, max_value=_HP_MAX)
    is_broken = serializers.BooleanField()
    problem_description = serializers.CharField(
        allow_null=True, allow_blank=True, required=False)

    def create(self,
               validated_data: Dict[str, Any]) -> Car:
        return Car.objects.create(**validated_data)

    def update(self, instance: Car,
               validated_data: Dict[str, Any]) -> Car:
        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)
        instance.save()
        return instance
