import string

from main.models import Users, Comments, Ratings


def password_db_check(username, password):
    user = Users.objects.filter(username=username, password=password)

    if user:
        return True, None
    else:
        return False, 'There is no such user or incorrect password.'


def username_in_db(username):
    user = Users.objects.filter(username=username).first()
    if user:
        return True, user
    else:
        return False, None


def username_identity(username):
    if Users.objects.filter(username=username).first():
        return False, 'Such user has already been registered.'
    elif len(username) > 29:
        return False, 'Username cannot be more than 30 characters.'
    elif ' ' in username:
        return False, 'Username cannot contain spaces.'
    elif not all(map(lambda char: char in string.ascii_letters, username)):
        return False, 'Username contains invalid characters.'
    else:
        return True, None


def get_user_id(username):
    user_id = Users.objects.filter(username=username).first().id
    return user_id


def passwords_identity(password_one, password_two):

    allowed_characters = string.ascii_letters + string.digits + string.punctuation

    if not password_one == password_two:
        return False, 'Passwords are not the same.'

    elif len(password_one) < 8:
        return False, 'Password must be at least 8 characters.'

    elif not all(map(lambda char: char in allowed_characters, password_one)):
        return False, 'Invalid characters in the password.'

    elif all(map(lambda char: char in string.ascii_letters, password_one)):
        return False, 'Password cannot contain only letters.'

    elif all(map(lambda char: char in string.digits, password_one)):
        return False, 'Password cannot contain only digits.'

    elif all(map(lambda char: char in string.punctuation, password_one)):
        return False, 'Password cannot contain only special simbols.'

    else:
        return True, None


def password_length(password):
    if len(password) >= 8:
        return True
    else:
        return False


def post_data_creation(post):
    creator = Users.objects.filter(id=post.user_id).first()

    created_at_data = post.created_at
    creation_date = created_at_data.date()
    creation_time = created_at_data.time()

    last_comment = Comments.objects.filter(post=post.id).order_by('-created_at').first()

    if last_comment:
        comment_creator = Users.objects.filter(id=last_comment.author_id).first()
    else:
        comment_creator = None

    post_id = post.id
    title = post.title
    content = post.content
    creator = creator.username
    last_comment = last_comment.content if last_comment else None
    comment_creator = comment_creator.username if comment_creator else None

    all_the_ratings_qs = Ratings.objects.filter(post_id=post_id).all()

    if not all_the_ratings_qs:
        rating = 0
    else:
        rating = avg_rating_determination(all_the_ratings_qs)

    stars = rating_formation(rating)

    post_data = {
        'id': post_id,
        'title': title,
        'content': content,
        'creation_date': creation_date,
        'creation_time': creation_time,
        'creator': creator,
        'last_comment': last_comment,
        'comment_creator': comment_creator,
        'rating': stars,
    }

    return post_data


def comments_on_post_collector(post_id):
    list_of_comments = []
    comments = Comments.objects.filter(post=post_id).order_by('-created_at')
    if comments:
        for comment in comments:
            id = comment.id
            creator = Users.objects.filter(id=comment.author_id).first().username
            content = comment.content
            created_at_data = comment.created_at
            creation_date = created_at_data.date()
            creation_time = created_at_data.time()

            if not comment.super_parent_comment:
                replied_comments = all_child_comments_for_super_parent(comment)
            else:
                replied_comments = []

            if not comment.parent_comment:

                comment_data = {
                    'id': id,
                    'creator': creator,
                    'content': content,
                    'creation_date': creation_date,
                    'creation_time': creation_time,
                    'replied_comments': replied_comments
                }

                list_of_comments.append(comment_data)

    return list_of_comments


def new_comment_db_push(post_id, comment_creator, comment_content):
    user = Users.objects.filter(username=comment_creator).first()
    user_id = user.id
    Comments.objects.create(post_id=post_id, author_id=user_id, content=comment_content)


def new_replied_comment_db_push(post_id, comment_creator, comment_content, parent_comment, super_parent_comment):
    user = Users.objects.filter(username=comment_creator).first()
    user_id = user.id
    Comments.objects.create(post_id=post_id, author_id=user_id, content=comment_content, parent_comment=parent_comment, super_parent_comment=super_parent_comment)


def all_child_comments_for_super_parent(super_parent_comment):
    all_child_comments = super_parent_comment.origins.order_by('created_at')

    replied_comments = []
    for reply in all_child_comments:
        created_at_data = reply.created_at
        replied_creator = Users.objects.filter(id=reply.author_id).first().username
        parent_comment = Comments.objects.get(pk=reply.parent_comment_id)
        parent_comment_author = Users.objects.filter(id=parent_comment.author_id).first().username
        reply_comment_info = {
            'id': reply.id,
            'creator': replied_creator,
            'content': reply.content,
            'creation_date': created_at_data.date(),
            'creation_time': created_at_data.time(),
            'replied_to': parent_comment_author
        }

        replied_comments.append(reply_comment_info)

    return replied_comments


def rating_formation(rating):
    filled_star = '<i class="fa-solid fa-star" style="color: rgb(113, 204, 218);"></i>'
    outlined_star = '<i class="fa-regular fa-star" style="color: rgb(113, 204, 218);"></i>'

    array_of_stars = []
    for filled_stars_counter in range(rating):
        array_of_stars.append({
            'value': filled_stars_counter + 1,
            'icon': filled_star,
        })

    for outlined_stars_counter in range(5 - rating):
        array_of_stars.append({
            'value': rating + outlined_stars_counter + 1,
            'icon': outlined_star,
        })

    return array_of_stars


def avg_rating_determination(ratings_qs):
    avg_rating = 0

    for rating in ratings_qs:
        avg_rating += rating.score

    result = avg_rating / len(ratings_qs)

    return round(result)