from django.shortcuts import render, redirect
from .models import Room # importer le modele
from .forms import RoomForm


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


# C R U D 
def createRoom(request):
    form = RoomForm() # importer le formulare

    if request.method =='POST':
        # print(request.POST) # Les donnees du form
        # print(request.POST.get('name')) # Les donnees d'un field dans le form
        form = RoomForm(request.POST)
        if form.is_valid(): # verifier si les données sont valides
            form.save() # on enregistre les données dans la BDD
            return redirect('home') # rediriger vers la page d'accueil

    context = {'form': form}
    return render (request, 'room_form.html', context)

def updateRoom(request, pk): # pk to know which item will be updated
    # query the room be updated
    room = Room.objects.get(id = pk)

    # le formulaire sera pré propulé des donnés du room de l'id qui correspond à pk
    form = RoomForm(instance=room) 

    if request.method =='POST':
        # print(request.POST) # Les donnees du form
        # print(request.POST.get('name')) # Les donnees d'un field dans le form

        # specifier le Room to be processed
        form = RoomForm(request.POST, instance=room)
        if form.is_valid(): # verifier si les données sont valides
            form.save() # on enregistre les données dans la BDD
            return redirect('home') # rediriger vers la page d'accueil

    context = {'form': form}
    return render (request, 'room_form.html', context)

def deleteRoom(request, pk):

    # savoir le room à supprimer
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete() # on supprimer le room de l'id conncerné
        return redirect('home')
    
    # on passe en context l'objet room à supprimer
    return render(request, 'delete.html', {'obj': room})

