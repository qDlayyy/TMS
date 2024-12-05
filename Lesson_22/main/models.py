from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=15, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    super_parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='origins'
    )


class Ratings(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

