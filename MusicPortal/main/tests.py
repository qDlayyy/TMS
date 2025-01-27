from django.test import TransactionTestCase
from django.contrib.auth.models import User
from .models import Genre, Artist, Album, Song, UserProfile


class GenreModelTest(TransactionTestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Rock")

    def test_string_representation(self):
        self.assertEqual(str(self.genre), "Rock")

    def test_unique_name(self):
        with self.assertRaises(Exception):
            Genre.objects.create(name="Rock")


class ArtistModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.artist = Artist.objects.create(user=self.user, name="Test Artist", bio="Bio of Test Artist")

    def test_string_representation(self):
        self.assertEqual(str(self.artist), "Test Artist")

    def test_artist_biography(self):
        self.assertEqual(self.artist.bio, "Bio of Test Artist")


class AlbumModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.artist = Artist.objects.create(user=self.user, name="Test Artist", bio="Bio of Test Artist")
        self.genre = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(title="Test Album", bio="Bio of Test Album")
        self.album.artists.add(self.artist)
        self.album.genres.add(self.genre)

    def test_string_representation(self):
        self.assertEqual(str(self.album), "Test Album")

    def test_album_relationships(self):
        self.assertIn(self.artist, self.album.artists.all())
        self.assertIn(self.genre, self.album.genres.all())


class SongModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.artist = Artist.objects.create(user=self.user, name="Test Artist", bio="Bio of Test Artist")
        self.genre = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(title="Test Album", bio="Bio of Test Album")
        self.song = Song.objects.create(title="Test Song", audio="test_audio.mp3", album=self.album)
        self.song.artists.add(self.artist)
        self.song.genres.add(self.genre)

    def test_string_representation(self):
        self.assertEqual(str(self.song), "Test Song")

    def test_song_relationships(self):
        self.assertIn(self.artist, self.song.artists.all())
        self.assertEqual(self.song.album, self.album)
        self.assertIn(self.genre, self.song.genres.all())


class UserProfileModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, bio="This is a test bio.")

    def test_string_representation(self):
        self.assertEqual(str(self.user_profile), "testuser")

    def test_user_profile_bio(self):
        self.assertEqual(self.user_profile.bio, "This is a test bio.")
