
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.post_view, name="post"),
    path("posts/<int:post_id>", views.get_post, name="get_post"),
    path("posts/create", views.create_post, name="create_post"),
]
