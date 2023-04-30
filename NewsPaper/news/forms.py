from django.forms import ModelForm,TextInput
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):


    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post

        fields = ['kind_of_post', 'header', 'main_text','category']
        widgets = {
            'post_author': TextInput(),
        }
