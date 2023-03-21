from django.forms import ModelForm
from .models import Room,User,Contact
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']
class RoomForm(ModelForm):
    class Meta:
        model = Room
        # all field of models
        fields = '__all__'
        exclude = ['host','participants']
class UserForm(ModelForm):
    class Meta:
        model = User  
        fields = ['avatar','name','username', 'email','bio']
    
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"
class RecoveryForm(ModelForm):
    class Meta:
        model = User
        fields =['email']
        
class PassCodeForm(UserCreationForm):
    class Meta:
        model = User
        fields =['password1',"password2"]