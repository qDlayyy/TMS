import uuid

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Artist, Song, Album


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Create a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})

        self.fields['username'].error_messages = {'required': 'All fields are required.'}
        self.fields['password1'].error_messages = {'required': 'All fields are required.'}
        self.fields['password2'].error_messages = {'required': 'All fields are required.'}

        for field in self.fields.values():
            field.help_text = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)
        UserProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})

        self.fields['username'].error_messages = {'required': 'All fields are required.'}
        self.fields['password'].error_messages = {'required': 'All fields are required.'}

        for field in self.fields.values():
            field.help_text = None


class ArtistRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArtistRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter your Artist Name'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Enter your bio'})

        self.fields['name'].error_messages = {'required': 'All fields are required.'}
        self.fields['bio'].error_messages = {'required': 'All fields are required.'}

        for field in self.fields.values():
            field.help_text = None

    class Meta:
        model = Artist
        fields = ['name', 'bio']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Artist.objects.filter(name=name).exists():
            raise "An artist with this name already exists. Please choose a different name."
        return name

    def save(self, user=None, commit=True):
        artist = super().save(commit=False)
        if user:
            artist.user = user
        if commit:
            artist.save()
        return artist


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['image']

    def save(self, commit=True):
        artist = super().save(commit)
        return artist


class AlbumPhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['image']

    def save(self, commit=True):
        album = super().save(commit)
        return album

class ArtistBio(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArtistBio, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'placeholder': 'Enter your bio'})

    class Meta:
        model = Artist
        fields = ['bio']


class UserBio(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserBio, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'placeholder': 'Enter your bio'})

    class Meta:
        model = UserProfile
        fields = ['bio']



class SongAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SongAddForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter a Song name'})
        self.fields['artists'].widget.attrs.update({'placeholder': 'Are there any other artists (use "," between them)?'})
        self.fields['genres'].widget.attrs.update({'placeholder': 'Enter a genre'})

        self.fields['title'].error_messages = {'required': 'All fields are required.'}
        self.fields['artists'].error_messages = {'required': 'All fields are required.'}
        self.fields['genres'].error_messages = {'required': 'All fields are required.'}

        for field in self.fields.values():
            field.help_text = None

    class Meta:
        model = Song
        fields = ['title', 'artists', 'audio', 'genres']


class AlbumCreation(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlbumCreation, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter an album title'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Album bio'})

        self.fields['title'].error_messages = {'required': 'All fields are required.'}
        self.fields['bio'].error_messages = {'required': 'All fields are required.'}


        for field in self.fields.values():
            field.help_text = None

    class Meta:
        model = Album
        fields = ['title', 'bio']


class SongToAlbumAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SongToAlbumAddForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter a Song name'})
        self.fields['artists'].widget.attrs.update({'placeholder': 'Are there any other artists (use "," between them)?'})
        self.fields['genres'].widget.attrs.update({'placeholder': 'Enter a genre'})

        self.fields['title'].error_messages = {'required': 'All fields are required.'}
        self.fields['artists'].error_messages = {'required': 'All fields are required.'}
        self.fields['genres'].error_messages = {'required': 'All fields are required.'}

        for field in self.fields.values():
            field.help_text = None





