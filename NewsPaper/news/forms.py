from django.forms import ModelForm,TextInput
from .models import Post,PostCategory,Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# from django.db import models




# Создаём модельную форму
class PostForm(ModelForm):


    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post

        fields = ['kind_of_post', 'header', 'main_text','category']
        widgets = {
            'post_author': TextInput(),
        }

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Users_group = Group.objects.get(name='Users')
        Users_group.user_set.add(user)
        return user

class SubscribeCategoryForm(ModelForm):
    class Meta:
        model = PostCategory
        fields = ['category']


