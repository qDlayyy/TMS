from django import forms

class UserLogInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLogInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Your password'})


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    second_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['second_password'].widget.attrs.update({'placeholder': 'Confirm the password'})


class PostChanger(forms.Form):
    title = forms.CharField(max_length=15)
    content = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'placeholder': 'Write your comment here...'})


class PostCreate(forms.Form):
    title = forms.CharField(max_length=15)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(PostCreate, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Post Title'})
        self.fields['content'].widget.attrs.update({'placeholder': 'Write your post data here...'})


class PostChange(forms.ModelForm):
    title = forms.CharField(max_length=15)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        super(PostChange, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Post Title'})
        self.fields['content'].widget.attrs.update({'placeholder': 'Write your post data here...'})

        if initial:
            self.fields['title'].widget.attrs.update({'placeholder': initial.get('title', 'Post Title')})
            self.fields['content'].widget.attrs.update({'placeholder': initial.get('content', 'Write your post data here...')})
