# Generated by Django 4.0.10 on 2023-06-16 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calbuddy_api', '0007_remove_meal_calorie_limit_exceeded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True, verbose_name='date joined'),
        ),
    ]
