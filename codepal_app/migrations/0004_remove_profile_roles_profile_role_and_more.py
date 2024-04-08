# Generated by Django 5.0.4 on 2024-04-08 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codepal_app', '0003_remove_profile_skills_profile_roles_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='roles',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('FS', 'Full Stack Developer'), ('FE', 'Front End Developer'), ('BE', 'Back End Developer'), ('UX', 'User Experience Designer')], default='FS', max_length=2, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='portfolio_link',
            field=models.CharField(max_length=1000, verbose_name='Portfolio Link'),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('project_image', models.CharField(max_length=1000, verbose_name='Project Image')),
                ('project_description', models.CharField(max_length=255, verbose_name='Project Description')),
                ('project_link', models.CharField(max_length=500, verbose_name='Project Link')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codepal_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200)),
                ('reviewed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='codepal_app.profile')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_written', to='codepal_app.profile')),
            ],
        ),
    ]
