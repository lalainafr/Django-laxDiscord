from django.db import models
from django.contrib.auth.models import User # import default django user model


class Room(models.Model): 
    #  user that hosts the room (default django user models)
    # User can host multiple rooms, room can have only 1 Host
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # topic can have multiple rooms, room can have only 1 topic
    # topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # allow it to be empty
    # when parent is deleted all the children (Room will, stay in the database and will be set to null)

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
        # null = True -> description in the BDD can be empty
        # blank = True -> FORM can be empty
    #participant =
    updated = models.DateTimeField(auto_now=True)
        #auto_now=True -> take a timestampevery time we save the instance
    created = models.DateTimeField(auto_now_add=True)
        #auto_now_add=True -> take  a timestamp when we first save or create the instance

    # string representation of the class
    def __str__(self):
        return str(self.name)