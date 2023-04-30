from django.urls import path
from .views import PostList, PostDetail,Search,AddPost,PostUpdateView,PostDeleteView

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostList.as_view(),name='news'),
    path('<int:pk>', PostDetail.as_view(),name='post'),
    path('search/', Search.as_view(),name='search'),
    path('add/', AddPost.as_view(),name='add'),
    path('<int:pk>/edit/',PostUpdateView.as_view(),name='edit'),
    path('<int:pk>/delete/',PostDeleteView.as_view(),name='delete'),
]
