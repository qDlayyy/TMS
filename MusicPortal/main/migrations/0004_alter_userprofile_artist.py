# Generated by Django 5.1.4 on 2024-12-16 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userprofile_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='artist',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.artist'),
        ),
    ]
