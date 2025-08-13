# cinema/serializers.py
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Car


class CarSerializer(serializers.Serializer):
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    horse_powers = serializers.IntegerField()
    is_broken = serializers.BooleanField()
    # може бути null і може бути відсутнім у вхідних даних
    problem_description = serializers.CharField(allow_null=True, required=False, allow_blank=True)

    def create(self, validated_data):
        """Створює Car та проганяє модельні валідатори (у т.ч. min/max для horse_powers)."""
        car = Car(**validated_data)
        try:
            car.full_clean()  # підхоплює MinValueValidator/MaxValueValidator з моделі
        except DjangoValidationError as e:
            # перетворюємо на DRF ValidationError
            raise serializers.ValidationError(e.message_dict or e.messages)
        car.save()
        return car

    def update(self, instance: Car, validated_data):
        """Оновлює Car з валідаторами моделі."""
        for field, value in validated_data.items():
            setattr(instance, field, value)
        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict or e.messages)
        instance.save()
        return instance
