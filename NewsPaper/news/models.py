from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Author
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
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='author_posts')
    kind_of_post = models.CharField(max_length=2,choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    header = models.CharField(default="",max_length=64)
    main_text = models.TextField(default="")
    post_rate = models.IntegerField(default=0)
    category = models.ManyToManyField(Category,through='PostCategory')

    def preview(self):
        return self.main_text[0:124] + "..."

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_query_name="categories_of_posts")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='post_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_comments')
    created_at = models.DateTimeField(default=today)
    comment_text = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(null = True, blank=True,default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()
