from django.contrib import admin

# Register your models here.

from .models import Meal, User

admin.site.register(Meal)
admin.site.register(User)
