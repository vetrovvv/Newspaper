from django.shortcuts import render
from django.views.generic import  DetailView,ListView,View,CreateView,UpdateView,DeleteView
from django_filters.views import FilterView
from .models import Post,PostCategory,Category,Author
from datetime import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .filters import PostFilter
from django_filters.views import BaseFilterView
from .forms import PostForm
from django.contrib.redirects.models import Redirect
from django.shortcuts import redirect




class PostList(ListView):

    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at_date']
    template_name = 'posts.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = PostFilter(self.request.GET,super().get_queryset()).qs
        return queryset



class AddPost(CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post_author = Author.objects.get(author = request.user.id)
            form.save()

        return redirect('/news')

class Search(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'search.html'
    ordering = ['-created_at_date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_queryset(self):
        queryset = PostFilter(self.request.GET,super().get_queryset()).qs
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context[
            'value1'] = self.object.post_author
        return context


