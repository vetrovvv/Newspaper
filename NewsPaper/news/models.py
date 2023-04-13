from django.db import models
from accounts.models import Author
from django.contrib.auth.models import User
from django.utils import timezone
today = timezone.now


class Category(models.Model):
    category = models.CharField(max_length = 200,unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NW'
    CHOICES = (
        (article,'Статья'),
        (news,'Новость'),
    )
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    kind_of_post = models.CharField(max_length=2,choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=64)
    main_text = models.TextField()
    post_rate = models.IntegerField(default=0)

    def preview(self):
        return self.main_text[0:124] + "..."

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()


class PostCategory(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=today)
    comment_text = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(null = True, blank=True)
