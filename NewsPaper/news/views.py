
from django.views.generic import  DetailView,ListView,CreateView,UpdateView,DeleteView
from .filters import PostFilter,CategFilter
from .forms import PostForm,SubscribeCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect,render,reverse
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMultiAlternatives
from datetime import datetime,timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from NewsPaper import settings
class PostList(ListView):

    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at_date']
    template_name = 'news/posts.html'
    paginate_by = 10
    form_class = SubscribeCategoryForm


    def get_queryset(self):
        queryset = PostFilter(self.request.GET,super().get_queryset()).qs
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscribeCategoryForm()
        return context





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
        if Post.objects.filter(
                post_author=Author.objects.get(author=request.user),
                created_at__gte=timezone.now() - timedelta(days=1),
        ).count() < 3:
            form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
            if form.is_valid():
                obj = form.save(commit=False)
                obj.post_author = Author.objects.get(author = request.user.id)
                form.save()
                url =Post.objects.filter().last().get_absolute_url()
                category_name = form.cleaned_data.get("category")[0]
                category = Category.objects.get(category=category_name)
                header = form.cleaned_data.get('header')
                preview = (form.cleaned_data.get('main_text'))[0:49] + "..."
                subject = header +' '+ preview
                href = 'http://127.0.0.1:8000'+ url
                for sub in category.subscribers.filter().exclude(email=''):
                    html_content = render_to_string(
                    'news/email_sub.html',
                        {
                    'subject': subject,
                    'href': href,
                        }
                    )
                    msg = EmailMultiAlternatives(
                        subject=f'Уважаемый {sub.username}! Новая статья в твоём любимом разделе!',
                        body=subject,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[sub.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            return redirect('/news/')
        else:
            send_mail(
                subject=f'{request.user.username},вы пытаетесь сделать более 3 постов в день!',
                message='Попробуйте через сутки!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email]
            )
            return redirect('/news/')


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

@login_required
def become_subscriber(request):
    if request.method == 'POST':
        form = SubscribeCategoryForm(request.POST)
        if form.is_valid():
            category = request.POST.get("category")
            sub = request.user
            category_addsub = Category.objects.get(pk=category)
            category_addsub.subscribers.add(sub)
            category_addsub.save()
    return redirect('/news/')

@login_required
def become_subscriber_detail(request):
    categories = request.POST.getlist('category')
    sub = request.user
    for category in categories:
        category_addsub = Category.objects.get(category=category)
        category_addsub.subscribers.add(sub)
        category_addsub.save()
    return redirect('/news/')




def redirect_view(request):
    response = redirect('http://127.0.0.1:8000/accounts/login/')
    return response
