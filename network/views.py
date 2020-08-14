from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, PostForm, Post, Like, Following, Follower


def index(request):
    CurrentUser = request.user
    CurrentUsPosts = Post.objects.filter(User=CurrentUser.id)
    Posts = Post.objects.all()
    paginator = Paginator(Posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    likecounts = []
    for x in page_obj:
        postpk = x.pk
        likecount = Like.objects.filter(Post=postpk).count()
        likecounts.append(likecount)
    #getcurrentuser's posts    
    queryList = []    
    HowMany = CurrentUsPosts.count()
    for z in range(HowMany):
        queryList.append(CurrentUsPosts[z].pk)
    rangex = range(1, paginator.num_pages + 1)    
    return render(request, "network/index.html", {
        "PostForm": PostForm,
        'page_obj': page_obj,
        "Like": Like,
        "CurrentUser": CurrentUser,
        "UserPost": queryList,
        "likecount": likecounts,
        "rangex": rangex,

    }) 


@csrf_exempt
@login_required
def NewPost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("Content", "")
        time = datetime.datetime.now().isoformat(" ", "seconds")
        CurrentUser = request.user
        x = Post(User=CurrentUser, Date=time, Content=content)
        x.save()
        return HttpResponseRedirect(reverse("index"))

@login_required
@csrf_exempt        
def EditPost(request):
    if request.method == "PUT": 
        data = json.loads(request.body)
        postid = data.get("id", "")
        x = Post.objects.get(pk=postid).Content
        return JsonResponse(x, safe=False)
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("Content", "")
        id = data.get("id", "")
        time = datetime.datetime.now().isoformat(" ", "seconds")
        x = Post.objects.get(pk=id)
        x.Content = content
        x.save()
        return JsonResponse("Saved Post", safe=False)      

@login_required        
def GetFollowingPosts(request, pk):
    CurrentUser = request.user
    Followings = Following.objects.filter(Follower=pk)
    NumFollowing = Followings.count()
    ## get all ids of followings
    l = []
    for a in range(NumFollowing):
        l.append(Followings[a].Following.id)
    ## count how many posts that user has, then filter the user's post and append them according to the count    
    queryList = []    
    for x in l:
        HowMany = Post.objects.filter(User=x).count()
        for z in range(HowMany):
            queryList.append(Post.objects.filter(User=x)[z])
    paginator = Paginator(queryList, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ##likes
    CurrentUsPosts = Post.objects.filter(User=pk)
    likecounts = []
    for x in page_obj:
        postpk = x.pk
        likecount = Like.objects.filter(Post=postpk).count()
        likecounts.append(likecount)
    #getFollowing/Posts   
    queryList = []    
    HowMany = CurrentUsPosts.count()
    for z in range(HowMany):
        queryList.append(CurrentUsPosts[z].pk)
    rangex = range(1, paginator.num_pages + 1)        
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        "x": "x",
        "UserPost": queryList,
        "likecount": likecounts,
        "rangex": rangex,
        "Like": Like,
        "CurrentUser": CurrentUser,
    })

@login_required(login_url='http://127.0.0.1:8000/login')
def GetUserProfile(request, pk):
    CurrentUser = request.user
    Posts = Post.objects.filter(User=pk)
    paginator = Paginator(Posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    Followed = User.objects.get(pk=pk)
    Followers = Follower.objects.filter(FollowedWho=pk)
    Followings = Following.objects.filter(Follower=Followed)
    CurrentUserFollowings = Following.objects.filter(Follower=CurrentUser)
    FollowerNum =  Followers.count()
    FollowingNum = Followings.count()
    ## get current user's following list but with user ids
    l = []
    for a in range(0, FollowerNum):
        l.append(Followers[a].Follower.id)
    if request.method == "POST":
        if CurrentUser.id not in l:
            x = Follower(Follower=CurrentUser, FollowedWho=Followed)
            z = Following(Follower=CurrentUser, Following=Followed)
            x.save()
            z.save()
            messages.success(request, 'Followed')
            return HttpResponseRedirect(reverse("userprofile", args=[pk]))
        else:
            Follower.objects.get(FollowedWho=Followed.id, Follower=CurrentUser.id).delete()
            Following.objects.get(Following=Followed.id, Follower=CurrentUser.id).delete()
            messages.success(request, 'Unfollowed')
            return HttpResponseRedirect(reverse("userprofile", args=[pk]))
    ##likes
    likecounts = []
    CurrentUsPosts = Post.objects.filter(User=CurrentUser.id)
    for x in page_obj:
        postpk = x.pk
        likecount = Like.objects.filter(Post=postpk).count()
        likecounts.append(likecount)
    #getSpecificUser's Posts 
    queryList = []    
    HowMany = CurrentUsPosts.count()
    for z in range(HowMany):
        queryList.append(CurrentUsPosts[z].pk)
    rangex = range(1, paginator.num_pages + 1)         
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        "x": "x",
        "Followers": Followers,
        "Following": Followings,
        "FollowingNum": FollowingNum,
        "FollowerNum": FollowerNum,
        "CurrentUser": CurrentUser,
        "ProfileOwner": Followed,
        "CurrentUserFollowings": CurrentUserFollowings,
        "l": l,
        "UserPost": queryList,
        "likecount": likecounts,
        "rangex": rangex,
        "Like": Like,
    })  

@csrf_exempt
def Likes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        userid = data.get("userid", "")
        postid = data.get("postid", "")
        post = Post.objects.get(pk=postid)
        user = User.objects.get(pk=userid)
        if Like.objects.filter(User=user, Post=post).exists():
            x = Like.objects.get(User=user, Post=post)
            x.delete()
            return JsonResponse("Unliked", safe=False)   
        else:
            x = Like(User=user, Post=post, Like=True)
            x.save()
            return JsonResponse("Liked", safe=False)   
@csrf_exempt            
def getLikes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postid = data.get("postid", "")
        postLike = Like.objects.filter(Post=postid).count()
        return JsonResponse(postLike, safe=False)

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
