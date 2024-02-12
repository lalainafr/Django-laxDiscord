from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm 



# create form for registration
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

# create MODELFORM for ROOM
class RoomForm(ModelForm):
    class Meta:
        model = Room # spécifier le modele
        fields = "__all__" #  specify all fields inside the model
        # fields = ['name', 'body'] #  specify  some fields inside the model
        exclude = ['host','participants'] # ne pas mettre ces champs dans le formulaire



# create MODELFORM for USER
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'bio', 'avatar']

