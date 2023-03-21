from django.db import models
from ChatRoom.models import User,Topic
# Create your models here.


class Post(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True, null=True)
    content = models.TextField()
    cover_img_id= models.CharField(max_length=255,null=True, blank=True)
    video = models.CharField(max_length=255,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(null=True, blank=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        if len(self.content) > 300:
            return self.content[0:300]
        else:
            return self.content
class Post_Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #set room id as foreign of Message rooom
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # use for ordering data

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        if len(self.body) > 50:
            return self.body[0:50]
        else:
            return self.body
    
    
