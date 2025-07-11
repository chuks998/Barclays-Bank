# Generated by Django 4.2.18 on 2025-03-21 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentifications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="default_profile.png",
                null=True,
                upload_to="profile_pics/",
            ),
        ),
    ]
