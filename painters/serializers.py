from rest_framework import serializers
from painters.models import Painting
from users.serializers import UserSerializer
from painters.models import Painting, Painter


# class PainterSerializer(serializers.ModelSerializer) :
    
#     class Meta :
#         model = Painter
#         fields = "__all__"

class ImageCreateSerializer(serializers.ModelSerializer) :
    # painter = PainterSerializer(many=True)
    
    class Meta :
        model = Painting
        fields = "__all__"
        read_only_fields=["user"]
        
class ConvertSerializer(serializers.ModelSerializer) :
    
    class Meta :
        model = Painting
        fields = "__all__"
        
