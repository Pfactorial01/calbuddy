# Generated by Django 4.2.2 on 2023-06-15 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("calbuddy_api", "0004_alter_user_managers_user_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="meal",
            name="calorie_limit_exceeded",
            field=models.BooleanField(
                default=False, verbose_name="calorie limit exceeded"
            ),
        ),
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True, verbose_name="date")),
                (
                    "calories_consumed",
                    models.IntegerField(default=0, verbose_name="calories consumed"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
