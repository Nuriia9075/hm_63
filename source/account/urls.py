from django.contrib.auth.views import LogoutView
from django.urls import path
from .views.member import RegisterView, ProfileDetailView, login_view, ToggleSubscribeView
from account.views.posts import PostAddView, UserSearchView, IndexView, ToggleLikeView, CommentADDView, PostDetailView

app_name = "account"

urlpatterns = [
    path('login/',login_view, name='login'),
    path('', IndexView.as_view(), name='index'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post_add/', PostAddView.as_view(), name="post_add"),
    path('search/',UserSearchView.as_view(), name='search'),
    path('profile/<int:pk>/supscribe/', ToggleSubscribeView.as_view(), name='toggle_subscribe'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('post/<int:pk>/add_comment/', CommentADDView.as_view(), name='add_comment'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

]