# Generated by Django 5.1.4 on 2024-12-12 21:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('bio', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='artists/')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('release_date', models.DateField()),
                ('image', models.ImageField(blank=True, upload_to='albums/')),
                ('artists', models.ManyToManyField(related_name='albums', to='main.artist')),
                ('genres', models.ManyToManyField(related_name='albums', to='main.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('audio', models.FileField(upload_to='songs/')),
                ('release_date', models.DateField()),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='main.album')),
                ('artists', models.ManyToManyField(related_name='songs', to='main.artist')),
                ('genres', models.ManyToManyField(related_name='songs', to='main.genre')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('favorite_albums', models.ManyToManyField(blank=True, related_name='favorite_albums', to='main.album')),
                ('favorite_artists', models.ManyToManyField(blank=True, related_name='favorite_artists', to='main.artist')),
                ('favorite_genres', models.ManyToManyField(blank=True, related_name='favorite_genres', to='main.genre')),
                ('favorite_songs', models.ManyToManyField(blank=True, related_name='favorite_songs', to='main.song')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
