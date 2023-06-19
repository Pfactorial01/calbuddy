from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Meal, User


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["name", "ingredients", "calories", "date"]
        optional_fields = ["calories", "date"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "daily_calorie_mark",
            "date_joined",
        ]
        optional_fields = ["daily_calorie_mark"]
