from django.urls import path
from .views import PostList, PostDetail,Search,AddPost,PostUpdateView,PostDeleteView,become_author,redirect_view,become_subscriber,become_subscriber_detail
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostList.as_view(),name='news'),
    path('<int:pk>',PostDetail.as_view(),name='post'),
    path('search/', Search.as_view(),name='search'),
    path('add/', AddPost.as_view(),name='add'),
    path('<int:pk>/edit/',PostUpdateView.as_view(),name='edit'),
    path('<int:pk>/delete/',PostDeleteView.as_view(),name='delete'),
    path('become_author/',become_author,name = "become_author"),
    path('login/',redirect_view,name='login'),
    path('become_subscriber/',become_subscriber,name = "become_subscriber"),
    path('become_subscriber_detail/',become_subscriber_detail,name = "become_subscriber_detail"),
]
