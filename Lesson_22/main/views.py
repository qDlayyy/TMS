from functools import wraps
from django.shortcuts import render, redirect
from .models import Posts, Users, Comments, Ratings
from .forms import CommentForm, UserRegistrationForm, UserLogInForm, PostCreate, PostChanger
from django.contrib import messages

from .service import post_data_creation, new_replied_comment_db_push, new_comment_db_push, comments_on_post_collector, \
    username_identity, passwords_identity, get_user_id, username_in_db, password_db_check


def session_required_decorator(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('username'):
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper


def home(request):
    list_of_post_datas = []
    posts = Posts.objects.all().order_by('-created_at')
    for post in posts:
        post_data = post_data_creation(post)
        list_of_post_datas.append(post_data)

    return render(request, 'main/index.html', {'posts': list_of_post_datas})


def about(request):
    return render(request, 'main/about.html')


def post_detailed(request, post_id):

    if request.session.get('is_replied') is None:
        request.session['is_replied'] = False

    post = Posts.objects.get(pk=post_id)
    post_data = post_data_creation(post)

    post_changer = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            username = request.session['username']
            content = comment_form.cleaned_data['content']

            if request.session.get('is_replied'):
                parent_comment_id = request.session.get('parent_comm_id')
                parent_comment = Comments.objects.get(pk=parent_comment_id)
                if parent_comment.super_parent_comment is None:
                    super_parent_comment = parent_comment
                else:
                    super_parent_comment = Comments.objects.get(pk=parent_comment.super_parent_comment.id)
                new_replied_comment_db_push(post_id, username, content, parent_comment, super_parent_comment)
            else:
                new_comment_db_push(post_id, username, content)

            request.session['is_replied'] = False

    list_of_comments = comments_on_post_collector(post_id)

    is_removal_and_update_allowed = is_post_delete_and_update_available(request,post_id)

    return render(request, 'main/post.html', {"form":post_changer, "post":post_data, "comments":list_of_comments, "is_removal_and_update_allowed": is_removal_and_update_allowed})


def registration(request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            password2 = registration_form.cleaned_data['second_password']

            is_username_available, error_message = username_identity(username)
            if not is_username_available:
                messages.error(request, error_message)
                return render(request, 'main/registration.html', {"form": registration_form})


            is_correct, error_message = passwords_identity(password, password2)
            if not is_correct:
                messages.error(request, error_message)
                return render(request, 'main/registration.html', {"form": registration_form})

            user = Users.objects.create(username=username, password=password)
            user_id = user.id
            request.session['user_id'] = user_id
            request.session['username'] = username
            return redirect('home')
        else:
            return render(request, 'main/registration.html', {"form": registration_form})

    else:
        registration_form = UserRegistrationForm()

    return render(request, 'main/registration.html', {"form":registration_form})


def log_in(request):
    if request.method == 'POST':
        log_in_form = UserLogInForm(request.POST)
        if log_in_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            is_username_available, error_message = username_in_db(username)
            is_password_correct, error_message = password_db_check(username, password)
            if not is_username_available:
                messages.error(request, 'There is no user with that username.')
                return render(request, 'main/log_in.html', {"form": log_in_form})

            if not is_password_correct:
                messages.error(request, error_message)
                return render(request, 'main/log_in.html', {"form": log_in_form})

            else:
                user_id = get_user_id(username)
                request.session['user_id'] = user_id
                request.session['username'] = username
                return redirect('home')

    else:
        log_in_form = UserLogInForm()

    return render(request, 'main/log_in.html', {"form": log_in_form})


def log_out(request):
    request.session['user_id'] = None
    request.session['username'] = None
    return redirect('home')


@session_required_decorator
def create_post(request):
    request.session['is_post_created'] = None
    if request.method == 'POST':
        post_creation = PostCreate(request.POST)
        if post_creation.is_valid():
            title = request.POST['title']
            content = request.POST['content']
            user_id = request.session['user_id']

            post = Posts.objects.create(title=title, content=content, user_id=user_id)
            request.session['is_post_created'] = True

            post_data = post_data_creation(post)
            return render(request, 'main/form_create.html', {"form": post_creation, "post": post_data})

        else:
            request.session['is_post_created'] = None
            return render(request, 'main/form_create.html', {"form": post_creation, "post": {}} )

    else:
        post_creation = PostCreate()

    return render(request, 'main/form_create.html', {'form': post_creation})


def update_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    post_data = post_data_creation(post)

    request.session['is_post_changed'] = None

    if request.method == 'POST':
        post_update = PostChanger(request.POST)
        if post_update.is_valid():
            title = request.POST['title']
            content = request.POST['content']

            Posts.objects.filter(id=post_id).update(title=title, content=content)
            post = Posts.objects.get(id=post_id)
            request.session['is_post_changed'] = True

            post_data = post_data_creation(post)

            return render(request, 'main/post_update.html', {"form": post_update, "post": post_data})
    else:
        initial = {'title': post_data["title"], 'content': post_data["content"]}
        post_update = PostChanger(initial=initial)

    return render(request, 'main/post_update.html', {"form": post_update,"post":post_data})


def delete_post(request, post_id):
    Posts.objects.get(pk=post_id).delete()
    return redirect('home')


def is_post_delete_and_update_available(request, post_id):
    owner = Posts.objects.filter(id=post_id).first().user_id
    if owner == request.session['user_id']:
        return True
    else:
        return False


def replied_comment(request, comment_id, post_id):
    request.session['is_replied'] = not request.session['is_replied']

    if request.session['is_replied']:
        request.session['parent_comm_id'] = comment_id
    else:
        request.session['parent_comm_id'] = None

    return redirect('post_detailed', post_id)


def rate_post(request, post_id, score):
    user_id = request.session['user_id']

    post_rating_by_user = Ratings.objects.filter(author_id=user_id, post_id=post_id).first()

    if not post_rating_by_user:
        Ratings.objects.create(author_id=user_id, post_id=post_id, score=score)
    else:
        Ratings.objects.filter(author_id=user_id, post_id=post_id).update(score=score)

    return redirect('post_detailed', post_id)






