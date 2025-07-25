# Generated by Django 4.2.18 on 2025-04-08 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("authentifications", "0005_customuser_account_ready"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date Joined"
            ),
        ),
    ]
