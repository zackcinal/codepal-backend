# Generated by Django 5.0.4 on 2024-04-11 19:07

import codepal_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codepal_app', '0008_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=codepal_app.models.upload_to),
        ),
    ]