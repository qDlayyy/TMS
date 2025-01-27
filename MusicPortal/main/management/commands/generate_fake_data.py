import os
import random
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from main.models import UserProfile, Artist, Genre, Album, Song


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        list_of_possible_genres = ['Pop', 'Rock', 'Hip Hop', 'R&B', 'Electronic', 'Jazz', 'Classic', 'Reggae', 'Metal']
        users_amount = 5
        bio_counter = 0

        for _ in range(users_amount):
            user = User.objects.create_user(
                username=faker.user_name(),
                password='password123',
            )

            is_bio = bool(random.randint(0, 1))

            user_profile = UserProfile.objects.create(
                user=user,
                bio=faker.text(max_nb_chars=100) if is_bio else '',
            )

            self.stdout.write(self.style.SUCCESS(f'NEW USER HAS BEEN CREATED ({user.username}).'))

            is_artist = bool(random.randint(0, 1))
            is_artist_bio = bool(random.randint(0, 1))

            if is_artist:
                artist = Artist.objects.create(
                    user=user,
                    name=faker.user_name(),
                    bio=faker.text(max_nb_chars=100) if is_artist_bio else '',
                )
                self.stdout.write(self.style.SUCCESS(f'NEW ARTIST HAS BEEN CREATED ({artist.name}) FOR USER {user.username}.'))

            if is_bio:
                bio_counter += 1

        genres = Genre.objects.all()
        print(list(genres))
        if not genres:
            for genre in list_of_possible_genres:
                genres = Genre.objects.create(
                    name=genre,
                )
            genres = Genre.objects.all()
            self.stdout.write(self.style.SUCCESS(f'{len(list_of_possible_genres)} NEW GENRES HAS BEEN CREATED.'))
        else:
            self.stdout.write(self.style.WARNING(f'NO NEW GENRES HAS BEEN CREATED.'))

        artists = Artist.objects.all()
        if not artists:
            self.stdout.write(self.style.WARNING(f'NO ARTISTS HAS BEEN CREATED. IMPOSSIBLE TO GENERATE SONGS AND ALBUMS. TRY TO INCREASE users_amount'))
        else:
            current_directory = Path(__file__).parent
            main_directory = current_directory.parent.parent
            songs_directory_path = os.path.join(main_directory, 'media', 'songs')
            list_of_songs = [file.name for file in Path(songs_directory_path).iterdir() if file.is_file()]

            number_of_artists_to_pick = random.randint(1, min(3, len(artists)))

            if list_of_songs:
                for song in list_of_songs:
                    current_song_path = Path(os.path.join('songs', song))
                    if not Song.objects.filter(audio=current_song_path).exists():
                        new_song = Song.objects.create(
                            title=faker.text(max_nb_chars=20),
                            audio=current_song_path.as_posix(),
                        )

                        sampled_genres = random.sample(list(genres), random.randint(1, len(list_of_possible_genres) - 1))
                        # sampled_genres_count = random.randint(1, max(1, len(genres)))
                        # sampled_genres = random.sample(list(genres.values_list('id', flat=True)), sampled_genres_count)
                        new_song.genres.set(sampled_genres)

                        sampled_artists = random.sample(list(artists), random.randint(1, number_of_artists_to_pick))
                        new_song.artists.set(sampled_artists)


                        self.stdout.write(self.style.SUCCESS(
                            f'SONG {new_song.title} HAS BEEN ADDED.'))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'CURRENT SONG EXISTS'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'SONGS CANNOT BE GENERATED. ADD AUDIO FILES'))

        self.stdout.write(self.style.SUCCESS(f'GENERATION DONE SUCCESSFULLY!'))