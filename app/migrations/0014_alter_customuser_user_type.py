# Generated by Django 5.0.6 on 2024-07-11 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_delete_timetable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[("1", "ADMIN"), ("2", "STAFF"), ("3", "STUDENT")],
                default="3",
                max_length=50,
            ),
        ),
    ]