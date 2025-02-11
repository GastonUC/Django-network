from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", db_index=True)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:50]}"
    
    class Meta:
        indexes = [
        models.Index(fields=['timestamp']),
        models.Index(fields=['user']),
        ]


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", db_index=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", db_index=True)
 
    def __str__(self):
        return f"{self.user} follows {self.follower}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes", db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes", db_index=True)

    def __str__(self):
        return f"{self.user} likes {self.post}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
        ]