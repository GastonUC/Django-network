from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import User, Post, Follower, Like


def index(request):
    if request.user.is_authenticated:
        feed = Post.objects.all()
        p = Paginator(feed, 10)
        return render(request, "network/index.html", {
            "feed": p.page(1),
            "likes": Like.objects.all().filter(user=request.user),
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required(login_url='/login')
def post_view(request):
    likes = Like.objects.all().filter(user=request.user)
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html", {
            "likes": likes
        })
    
@login_required(login_url='/login')
def load_post():
    feed = Post.objects.all()
    p = Paginator(feed, 10)
    posts = list(Post.objects.values())
    return JsonResponse(posts, safe=False, status=200)

def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return JsonResponse({"id": post.id, "user": post.user.id, "content": post.content, "created_at": post.timestamp})

def profile(request, username):
    return render(request, "network/profile.html", {
        "user": User.objects.get(username=username),
    })

def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return JsonResponse({"message": "Post created successfully."})
        # return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
