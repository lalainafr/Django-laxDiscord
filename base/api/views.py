# from django.http import JsonResponse


# def getRoutes(request): # route of the API
#     routes = [
#         'GET /api' 
#         'GET /api/rooms' # list of rooms
#         'GET /api/room/:id' # room detail
#     ]
#     return JsonResponse(routes, safe=True)
#     # safe=False -> we ca use more than python dictionnary inside the response

# TUILISER DJANGO FRAMEWORK
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# methode acceptée
@api_view(['GET'])
def getRoutes(request): # route of the API
     routes = [
         'GET /api' 
         'GET /api/rooms' # list of rooms
         'GET /api/room/:id' # room detail
     ]
     return Response(routes)

@api_view(['GET'])
def getRooms(request):
     rooms =  Room.objects.all()
     serializer = RoomSerializer(rooms, many=True)
     return Response(serializer.data)

     
@api_view(['GET'])
def getRoom(request, pk):
     rooms =  Room.objects.get(id=pk)
     serializer = RoomSerializer(rooms, many=False)
     return Response(serializer.data)

     