from typing import Any, Dict
from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    horse_powers = serializers.IntegerField()
    is_broken = serializers.BooleanField()
    problem_description = serializers.CharField(
        allow_null=True, allow_blank=True, required=False)

    def create(self, validated_data: Dict[str, Any]) -> Car:
        return Car.objects.create(**validated_data)

    def update(self, instance: Car,
               validated_data: Dict[str, Any]) -> Car:
        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)
        instance.save()
        return instance
