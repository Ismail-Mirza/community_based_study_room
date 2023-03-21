from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    username= models.CharField(unique=True,max_length=200, null=True)
    email = models.EmailField(unique=True,null=True)
    is_writer = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    # avatar = models.ImageField(null=True, default="avatar.svg")
    avatar = CloudinaryField('image',null=True,default="avatar.svg")
    # default login options
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    #bigger text field
    #null True mean description filed can be blank
    #blank=True mean form can be blank
    description = models.TextField(null=True, blank=True)
    # participants =
    #update we will make changes and django will update automatically
    # auto_now take snap shot every time after update
    updated = models.DateTimeField(auto_now=True)
    # add participants list in the Room blank =True use for submit form without check
    participants = models.ManyToManyField(
        User, related_name="participants", blank=True)
    #auto_now_add=True take snap shot while created
    created = models.DateTimeField(auto_now_add=True)
    # use for ordering data

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #set room id as foreign of Message rooom
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # use for ordering data

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Contact(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
