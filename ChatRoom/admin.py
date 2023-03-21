from django.contrib import admin

# Register your models here.
from .models import Room, User, Topic, Message,Contact
#register with the admin panel
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Contact)
