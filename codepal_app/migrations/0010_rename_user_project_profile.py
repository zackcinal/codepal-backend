# Generated by Django 5.0.4 on 2024-04-12 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepal_app', '0009_profile_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='profile',
        ),
    ]