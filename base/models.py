from django.db import models
# from django.contrib.auth.odels import User # import default django user model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='blog.jpg' )

    USERNAME_FIELD = 'email' # le user sera identifié par son email
    REQUIRED_FIELDS = []


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model): 
    #  user that hosts the room (default django user models)
    # User can host multiple rooms, room can have only 1 Host
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # topic can have multiple rooms, room can have only 1 topic
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True) # allow it to be empty
    # when parent is deleted all the children (Room will, stay in the database and will be set to null)

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
        # null = True -> description in the BDD can be empty
        # blank = True -> FORM can be empty
    
    # relation MANY TO MANY, foreign key avec le nom du parent
    # un participant peut avoir plusieurs room et vice versa
    participants = models.ManyToManyField(User, related_name='paricipants')
    # related_name: parce que User esr déjà utilisé dans le host

    updated = models.DateTimeField(auto_now=True)
        #auto_now=True -> take a timestampevery time we save the instance
    created = models.DateTimeField(auto_now_add=True)
        #auto_now_add=True -> take  a timestamp when we first save or create the instance
    

    # render new item first
    class Meta:
        ordering = ['-updated', '-created']
        # reverse ordering
        # order to show the newest room first

    # string representation of the class
    def __str__(self):
        return str(self.name)
    

class Message(models.Model):
    # user that send the message
    # we use first the django default user models
    # create ony to many relationship 
    user =  models.ForeignKey(User, on_delete=models.CASCADE) 

    # when parent is deleted all the children (message wilL be deleted as well)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 

    body = models.TextField()
    
    updated = models.DateTimeField(auto_now=True)
        #auto_now=True -> take a timestampevery time we save the instance
    created = models.DateTimeField(auto_now_add=True)
        #auto_now_add=True -> take  a timestamp when we first save or create the instance

 # render new item first
    class Meta:
        ordering = ['-updated', '-created']
        # reverse ordering
        # order to show the newest message first

    # string representation of the class
    def __str__(self):
        return self.body[0:50] # first 50 caracters
