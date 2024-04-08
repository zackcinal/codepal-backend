# Generated by Django 5.0.4 on 2024-04-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codepal_app', '0002_alter_profile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='skills',
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.CharField(choices=[('FS', 'Full Stack Developer'), ('FE', 'Front End Developer'), ('BE', 'Back End Developer'), ('UX', 'User Experience Designer')], default='FS', max_length=2, verbose_name='Roles'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_developer',
            field=models.BooleanField(verbose_name='Are You a Developer?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=30, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='portfolio_link',
            field=models.CharField(max_length=100, verbose_name='Portfolio Link'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.CharField(max_length=1000, verbose_name='Profile Picture'),
        ),
    ]
