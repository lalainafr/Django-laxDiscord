from rest_framework.serializers import ModelSerializer
from base.models import Room

# convert python object datat to json
# so taht it can be returned by the api
class RoomSerializer(ModelSerializer):
    class Meta:
        model =  Room
        fields = '__all__'