# Generated by Django 4.0.10 on 2023-06-15 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calbuddy_api', '0002_day_alter_meal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date'),
        ),
        migrations.DeleteModel(
            name='Day',
        ),
    ]
