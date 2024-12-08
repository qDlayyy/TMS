import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lesson_22.settings")
django.setup()

from django_seed import Seed
from main.models import Users, Posts, Comments, Ratings

def seed_users(number=20):
    seeder = Seed.seeder()

    seeder.add_entity(Users, number,
                      {
                         'username': lambda username: seeder.faker.user_name(),
                         'password': lambda password: seeder.faker.password(),
                         'created_at': lambda created_at: seeder.faker.date(),
                      }
                      )

    seeder.execute()

def seed_posts(number=20):
    seeder = Seed.seeder()

    users = Users.objects.all()

    seeder.add_entity(Posts, number,{
        'title': lambda title: seeder.faker.sentence(),
        'user': lambda username: random.choice(users),
        'content': lambda content: seeder.faker.text(),
        'created_at': lambda created_at: seeder.faker.date(),
    })

    seeder.execute()


def seed_comments(number=50):

    seeder = Seed.seeder()

    posts = Posts.objects.all()
    users = Users.objects.all()

    for comment in range(number):
        post = random.choice(posts)
        comments = Comments.objects.filter(post=post)

        if comments:
            is_the_comment_parent = random.choice([True, False])

            if is_the_comment_parent:
                parent_comment = None
                super_parent_comment = None

            else:
                only_parent_comments = Comments.objects.filter(post=post, parent_comment=None)

                if only_parent_comments:
                    parent_comment = random.choice(only_parent_comments)
                else:
                    parent_comment = random.choice(comments)

                is_reply_to_parent_comment = random.choice([True, False])
                if is_reply_to_parent_comment:
                    super_parent_comment = parent_comment

                else:
                    replied_comments = Comments.objects.filter(post=post).exclude(parent_comment=None)

                    if replied_comments:
                        parent_comment = random.choice(replied_comments)
                        super_parent_comment_id = parent_comment.super_parent_comment.id
                        super_parent_comment = Comments.objects.get(id=super_parent_comment_id)
                    else:
                        super_parent_comment = parent_comment

        else:
            parent_comment = None
            super_parent_comment = None

        seeder.add_entity(Comments, 1,{
            'post': post,
            'author': lambda username: random.choice(users),
            'content': lambda content: seeder.faker.text(),
            'created_at': lambda created_at: seeder.faker.date(),
            'parent_comment': parent_comment,
            'super_parent_comment': super_parent_comment
        })

        seeder.execute()


def seed_ratings(number=50):
    seeder = Seed.seeder()
    posts = Posts.objects.all()
    users = Users.objects.all()

    seeder.add_entity(Ratings, number,{
        'post': lambda post: random.choice(posts),
        'author': lambda username: random.choice(users),
        'score': lambda score: seeder.faker.random_int(1, 5),
        'created_at': lambda created_at: seeder.faker.date(),
    })

    seeder.execute()



if __name__ == "__main__":
    seed_users()
    seed_posts()
    seed_comments()
    seed_ratings()