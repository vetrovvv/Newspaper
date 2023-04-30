from django_filters import FilterSet,DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post,Author,User
from datetime import datetime, timedelta



# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {'created_at_date':['gte'],
                  'post_rate':['gte'],
                  'post_author_id': ['exact'],
                 }
