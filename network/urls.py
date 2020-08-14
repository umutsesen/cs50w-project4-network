
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:pk>", views.GetUserProfile, name="userprofile"),
    path("following/<int:pk>", views.GetFollowingPosts, name="GetPosts"),



    ## APIs
    path("postnew", views.NewPost, name="newpost"),
    path("EditPost", views.EditPost, name="editpost"),
    path("Likes", views.Likes, name="Like"),
    path("getLikeCount", views.getLikes, name="getlike")
   
]
