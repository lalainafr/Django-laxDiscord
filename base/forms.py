from django.forms import ModelForm
from .models import Room


# create MODELFORM
class RoomForm(ModelForm):
    class Meta:
        model = Room # spécifier le modele
        fields = "__all__" #  specify all fields inside the model
        # fields = ['name', 'body'] #  specify  some fields inside the model
