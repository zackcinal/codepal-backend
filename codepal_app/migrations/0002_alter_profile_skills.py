# Generated by Django 5.0.4 on 2024-04-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codepal_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.CharField(choices=[('FS', 'Full Stack Developer'), ('FE', 'Front End Developer'), ('BE', 'Back End Developer'), ('UX', 'User Experience Designer')], default='FS', max_length=2, verbose_name='Skills'),
        ),
    ]
