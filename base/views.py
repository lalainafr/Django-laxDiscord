from django.shortcuts import render, redirect
from django.contrib import messages # flash message
from django.contrib.auth import authenticate, login, logout # importer auth, logout et login methods
from django.db.models import Q # import the Q lookup method
# from django.contrib.auth.models import User --> user par defaut de django
from .models import Room, Topic, Message,User # importer les modele, u compris custom User 
from django.contrib.auth.decorators import login_required # restreoindre accès
from django.http import HttpResponse

# default user creaation form
# on le mets dans form directement
# from django.contrib.auth.forms import UserCreationForm # 

# mettre le new form créer dans forms.py
from .forms import RoomForm, UserForm, MyUserCreationForm


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
    # form = UserCreationForm() --> replace to MyUserRegistrationForm
    form = MyUserCreationForm()

    # traiter le formulaire
    if request.method == 'POST':

        # on créer le formulaire à partir de tous le credential (username, password...)
        form = MyUserCreationForm(request.POST)
        # UserCreationForm() --> replace to MyUserRegistrationForm

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

    # Q lookup method
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

    # liste des messages d'un room pour le RECENT ACTIVITY template
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))
    # on utile le Q pour filtrer par topic recent activity

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    # données à faire passer danns le template

    return render(request,'home.html', context)

def room(request, pk): # on passe le primary pour la valeur dynamique en paramètre)
    room = Room.objects.get(id = pk)

    participants = room.participants.all
    # acceder aux participants

    room_messages = room.message_set.all().order_by('-created') 
    # ordered by the most recent message 
    # query child object of a specific room
    # give the message set to this room

    # Créer le message tapé par l'utilisateur
    # traiter le formulaire
    if request.method =='POST':
        # créer un message
        message = Message.objects.create(
            # set the room, user and the body field
            user = request.user,
            room = room,
            body = request.POST.get('body')
            # recupérer le body tapé du formulaire
        )   

        # rajouter le participant qui a posté un commentaire
        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    # room = None
    # for i in rooms: # on boucle sur la liste des rooms
    #     if i['id'] == int(pk): # s'il y a un id qui match avec le pk (primary key)
    #         room = i # on prend sa valeur et on le passe dans le context du template
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    return render(request,'room.html', context)

def userProfile(request, pk):
    # reccueuillir touts les informations sur le user
    user = User.objects.get(id=pk)
    
    # acceder à des données des enfants de l'objet
    rooms = user.room_set.all() # pour le volet 'feed_compoenent' dans le profile
    room_messages = user.message_set.all() # pour le volet 'participant_component' dans le profile

    topics = Topic.objects.all() # pour le volet 'topic search' dans profile

    context = {'user' : user, 'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'profile.html', context)

# C R U D 

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm() # importer le formulare

    # on prend la liste des topics et on les passe en contexte
    # pour le dropdown du template
    topics = Topic.objects.all() 

    if request.method =='POST':
        # customise form
        topic_name =  request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # va retourner un objet ou bien va retourner un ojbet et le créera apres dans le dropdown

        # On utilisera la methode 'create' car on doit customiser la section 'topic'
        Room.objects.create(
            host =  request.user,
            topic =  topic, # on aura soit le new topic, ou ceux dans la bdd
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        return redirect('home') # rediriger vers la page d'accueil

        # ON NE VA PAS UTILISER LE FORMULAIRE NORMAL
        # print(request.POST) # Les donnees du form
        # print(request.POST.get('name')) # Les donnees d'un field dans le form
        # form = RoomForm(request.POST)
        # if form.is_valid(): # verifier si les données sont valides
        #     room = form.save(commit=False) # on enregistre plustard les données dans la BDD
        #     # on fait un traitement avant de faire le commit
        #     room.host = request.user
        #     room.save()
            

    context = {'form': form, 'topics': topics}
    return render (request, 'room_form.html', context)

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
@login_required(login_url='login')
def updateRoom(request, pk): # pk to know which item will be updated
    # query the room be updated
    room = Room.objects.get(id = pk)

    # le formulaire sera pré propulé des donnés du room de l'id qui correspond à pk
    form = RoomForm(instance=room) 

      # on prend la liste des topics et on les passe en contexte
    # pour le dropdown du template
    topics = Topic.objects.all() 

    # Only the host user can update his room
    if request.user != room.host:
        return HttpResponse('Your are not allowed to update this room')    

    if request.method =='POST':
        #  process the form
         # customise form
        topic_name =  request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # va retourner un objet ou bien va retourner un ojbet et le créera apres dans le dropdown
        
        # get the model and update the values
        room.name = request.POST.get('name')
        room.topic = topic # the topic that was created above
        room.description = request.POST.get('description')   

        room.save()    

        # print(request.POST) # Les donnees du form
        # print(request.POST.get('name')) # Les donnees d'un field dans le form

        # specifier le Room to be processed
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid(): # verifier si les données sont valides
        #     form.save() # on enregistre les données dans la BDD
        return redirect('home') # rediriger vers la page d'accueil

    context = {'form': form,'topics': topics, 'room': room}
    return render (request, 'room_form.html', context)

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
# supprimer un room
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

# supprimer un message
def deleteMessage(request, pk):
    
    # savoir le message à supprimer
    message = Message.objects.get(id = pk)

    # Only the host user can delete his room
    if request.user != message.user:
        return HttpResponse('Your are not allowed to update this room')    
    
    if request.method == 'POST':
        message.delete() # on supprimer le room de l'id conncerné
        return redirect('home')
    
    # on passe en context l'objet room à supprimer
    return render(request, 'delete.html', {'obj': message})
    # le template 'delete.html' c'est un template DYNAMIQUE 
    # servira pour effectuer un delete sur n'importe quel objet (message, room...)

# l'uitlisateur doit est connecté
# sinon redirigé vers la page 'login'
# supprimer un room
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    # le formulaire sera pré propulé des donnéss du user connecté 
    form = UserForm(instance=user)   

    # process form
    if request.method =='POST':
        # specifier le Room to be processed
        form = UserForm(request.POST, request.FILES, instance=user)
        # envoyer dans le formulare aussi le FILE
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk= user.id )
    context = {'form': form}
    return render(request, 'update_user.html', context)
