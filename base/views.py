from django.shortcuts import render, redirect
from django.contrib import messages # flash message
from django.contrib.auth import authenticate, login, logout # importer auth, logout et login methods
from django.db.models import Q # import the Q lookup method
from django.contrib.auth.models import User
from .models import Room, Topic # importer le modele
from .forms import RoomForm
from django.contrib.auth.decorators import login_required # restreoindre accès
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# Données (hardcoded)
# rooms = [
#     {'id': 1 , 'name': 'Lets learn puthon'},
#     {'id': 2 , 'name': 'Design with me'},
#     {'id': 3 , 'name': 'frontend developers'}
# ]

# formualire de login
def loginPage(request):

    # identifier la page de login
    page = 'login '

    if request.user.is_authenticated:
        return redirect('home')

    # traiter le formulaire
    if request.method == 'POST':
        # Récuperer le nom et le mdp dans le formulaire
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # vérifier si l'utilisateur existe (try/except)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does no exist.") # message flash

        # Verifier si e credentials sont corrects
        user = authenticate(request, username=username, password=password)        

        # si l'utilisateur existe on fait l'authentification et la redirection
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exists") # message flash

    context = {'page': page}
    return render(request, 'login_register.html', context)    

# registration
def registerPage(request):

    # créer le form registration
    form = UserCreationForm()

    # traiter le formulaire
    if request.method == 'POST':

        # on créer le formulaire à partir de tous le credential (username, password...)
        form = UserCreationForm(request.POST)


        if form.is_valid(): # on verifie si le formulaire est valide
            user = form.save(commit=False) # on va encore traiter l'objet
            user.username = user.username.lower() # on met le username en lowercase
            user.save() # on enregistre les donneés en bdd
            login(request, user)  # on log le user juste après l'inscription
            redirect('home') # on redirige le user vers la page d'accueil
        else:
            messages.error(request, "An error occured during registration") # message flash        

    context = {'form': form}
    return render(request, 'login_register.html', context)
    
# logout
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):

    # q = whatever we passed in the url
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Q llookup method
    rooms = Room.objects.filter(
        # on peux faire plusieurs filtre avec le '&' ou '|'
        # -> contient le contenu du 'q' soit sur le topic, la description  ou le nom du room
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        ) 
    
    # provides filtered Rooms in the database by topic name
    # topic__name = value of topic.name
    # topic__name__icontains = value contained in topic.name
    # rooms = Room.objects.filter(topic__name__icontains = q) 

    # model manager 'Object' to make a query with the model
    # rooms = Room.objects.all() # provides all Rooms in the database

    # liste des topic à mettre sur le sodebar pour le search
    topics = Topic.objects.all()

    # compter le nombre de room et le passer dans le context pour le template
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    # données à faire passer danns le template

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

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
@login_required(login_url='login')
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

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
@login_required(login_url='login')
def updateRoom(request, pk): # pk to know which item will be updated
    # query the room be updated
    room = Room.objects.get(id = pk)

    # le formulaire sera pré propulé des donnés du room de l'id qui correspond à pk
    form = RoomForm(instance=room) 

    # Only the host user can update his room
    if request.user != room.host:
        return HttpResponse('Your are not allowed to update this room')    

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

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
@login_required(login_url='login')
def deleteRoom(request, pk):

    # savoir le room à supprimer
    room = Room.objects.get(id = pk)

    # Only the host user can delete his room
    if request.user != room.host:
        return HttpResponse('Your are not allowed to update this room')    
    
    if request.method == 'POST':
        room.delete() # on supprimer le room de l'id conncerné
        return redirect('home')
    
    # on passe en context l'objet room à supprimer
    return render(request, 'delete.html', {'obj': room})

