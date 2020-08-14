from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Post(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    Content = models.TextField(blank=False)
    Date = models.DateTimeField(blank=False)
    
    def serialize(self):
        return {
            "PostId": self.id,
            "Poster": self.User.username,
            "Content": self.Content,
            "Date": self.Date,
        }
        

class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Content'].widget.attrs.update({'class': 'form-control'})
        self.fields['Content'].widget.attrs.update({'rows': '3'})
        self.fields['Content'].widget.attrs.update({'cols': '10'})
        
    class Meta:
        model = Post
        fields = ["Content"]
        

class Like(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postlike")
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userlike")
    Like = models.IntegerField(default=0) 

class Follower(models.Model):
    FollowedWho = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Followed")
    Follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FollowerUser")
    
    def __str__(self):
        return f"{self.Follower}"

class Following(models.Model):
    Follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="RealFollower")
    Following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="WhoFollowed")
    
    def __str__(self):
        return f"{self.Following}"