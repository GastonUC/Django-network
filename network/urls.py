
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.load_post, name="post"),
    path("posts/create", views.create_post, name="create"),
    path("posts/<int:post_id>", views.get_post, name="get_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("posts/feed", name="feed"),
    path("posts/following", name="following"),
]
