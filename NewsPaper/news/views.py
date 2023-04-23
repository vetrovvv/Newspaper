from django.shortcuts import render
from django.views.generic import \
    ListView, DetailView,TemplateView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post,Author,Category,PostCategory
from datetime import datetime
from django.contrib.auth.models import User


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-created_at').values()




class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context[
            'value1'] = self.object.post_author.author.username
        return context


