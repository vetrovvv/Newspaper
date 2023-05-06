
from django.views.generic import  DetailView,ListView,CreateView,UpdateView,DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect

class PostList(ListView):

    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at_date']
    template_name = 'news/posts.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = PostFilter(self.request.GET,super().get_queryset()).qs
        return queryset



class AddPost(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',
                           )
    model = Post
    template_name = 'news/add.html'
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
    template_name = 'news/search.html'
    ordering = ['-created_at_date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',
                           )
    model = Post
    template_name = 'news/post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',
                           )
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_queryset(self):
        queryset = PostFilter(self.request.GET,super().get_queryset()).qs
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None,**kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context[
            'value1'] = self.object.post_author
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(author=request.user,author_rate=0)
    return redirect("/news/")


def redirect_view(request):
    response = redirect('http://127.0.0.1:8000/accounts/login/')
    return response