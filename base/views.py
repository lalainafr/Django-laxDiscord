from django.shortcuts import render
from .models import Room # importer le modele

# Create your views here.

# Données (hardcoded)
# rooms = [
#     {'id': 1 , 'name': 'Lets learn puthon'},
#     {'id': 2 , 'name': 'Design with me'},
#     {'id': 3 , 'name': 'frontend developers'}
# ]

def home(request):
    # model manager 'Object' to make a query with the model
    rooms = Room.objects.all() # provides all Rooms in the database

    context = {'rooms': rooms}
    # passer les données de la liste dans le template
    return render(request,'home.html', context)

def room(request, pk): # on passe le primary pour la valeur dynamique en paramètre)
    room = Room.objects.get(id = pk)
    # room = None
    # for i in rooms: # on boucle sur la liste des rooms
    #     if i['id'] == int(pk): # s'il y a un id qui match avec le pk (primary key)
    #         room = i # on prend sa valeur et on le passe dans le context du template
    context = {'room': room}

    return render(request,'room.html', context)
