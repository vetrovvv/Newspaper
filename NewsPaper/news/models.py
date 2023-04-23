from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
today = timezone.now
from django.db.models import Sum
from datetime import *


saver = []   # List of dictionaries that gets the rating of all comments on the author's posts and is cleared when getCommentsOfAuthorPosts completes
try:
    del saver[0]
except IndexError:
    pass
def getCommentsRateOfAuthorPosts():
        for e in saver:
            return e.get('comment_rate__sum')


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.IntegerField(null = True, blank=True)



    def update_rating(self):
        post_rating = self.author_posts.all().aggregate(Sum('post_rate'))
        post_rating_multiplied = post_rating.pop('post_rate__sum') * 3
        author_comments_rating_dict = self.author.user_comments.all().aggregate(Sum('comment_rate'))
        author_comments_rating = author_comments_rating_dict.get('comment_rate__sum')
        posts_of_author = self.author_posts.all()

        for post in posts_of_author:
            comset = post.post_comments.all()
            saver.append(comset.aggregate(Sum('comment_rate')))

        final_rate = post_rating_multiplied + author_comments_rating + getCommentsRateOfAuthorPosts()

        self.author_rate = final_rate
        self.save()

    def __str__(self):
        return f'{self.category.title()}'
class Category(models.Model):
    category = models.CharField(max_length = 200,unique=True)

    def __str__(self):
        return f'{self.category.title()}'

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
    category = models.ManyToManyField(to='Category',through='PostCategory')


    def __str__(self):
        l = self.post_author.author.username
        time = self.created_at.strftime("%d:%m:%Y:%H:%M")
        return f'Автор {l}:={self.header.title()}{self.main_text}{time}'



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
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="categories_of_posts")

    def __str__(self):
        return f'{self.category.title()}'

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


