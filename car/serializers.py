from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.Serializer):
    # порядок полів важливий (тести очікують id першим)
    id = serializers.IntegerField(read_only=True)
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    horse_powers = serializers.IntegerField()  # валідатори меж спрацюють на рівні моделі
    is_broken = serializers.BooleanField()
    problem_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance