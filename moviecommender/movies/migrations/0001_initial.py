# Generated by Django 3.2.3 on 2021-05-31 16:35

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import moviecommender.movies.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('title', models.CharField(max_length=250)),
                ('summary', models.TextField(blank=True, null=True)),
                ('cast', models.CharField(max_length=100)),
                ('genre', models.CharField(blank=True, choices=[('ACTION', 'ACTION'), ('ADVENTURE', 'ADVENTURE'), ('ART_HOUSE', 'ART_HOUSE'), ('COMEDY', 'COMEDY'), ('MYSTERY', 'MYSTERY'), ('FANTASY', 'FANTASY'), ('HISTORICAL', 'HISTORICAL'), ('HORROR', 'HORROR'), ('ROMANCE', 'ROMANCE'), ('SATIRE', 'SATIRE'), ('BLACK_COMEDY', 'BLACK_COMEDY'), ('SCI_FI', 'SCI_FI'), ('THRILLER', 'THRILLER'), ('WESTERN', 'WESTERN'), ('DOCUMENTARY', 'DOCUMENTARY'), ('MUSICAL', 'MUSICAL'), ('TV_SERIES', 'TV_SERIES'), ('INDIE', 'INDIE')], max_length=25, null=True)),
                ('director', models.CharField(max_length=100)),
                ('writer', models.CharField(max_length=100)),
                ('main_cast', models.CharField(blank=True, max_length=100, null=True)),
                ('mpaa_rating', models.CharField(max_length=12)),
                ('cinematographer', models.CharField(max_length=100)),
                ('prod_company', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=moviecommender.movies.models.get_movie_picture_upload_path)),
                ('imdb_rating', models.PositiveIntegerField(blank=True, null=True)),
                ('rt_rating', models.PositiveIntegerField(blank=True, null=True)),
                ('metacritic_rating', models.PositiveIntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=25, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieWatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_by', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies_moviewatchlist_created', to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_watchlist', to='movies.movie')),
                ('updated_by', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies_moviewatchlist_modified', to=settings.AUTH_USER_MODEL)),
                ('watcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_watcher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated_at',),
                'abstract': False,
            },
        ),
    ]
