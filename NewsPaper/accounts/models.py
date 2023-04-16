from django.db import models
from django.contrib.auth.models import User
import news.models
from django.db.models import Sum


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




