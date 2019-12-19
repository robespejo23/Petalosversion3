#que es un serializador en django
# bbdd datos json
# json datos bdd
#rest_framework
from rest_framework import serializers
from . models import Flores

class FloresSerializer(serializers.ModelSerializer):
    class Meta :
        model = Flores
        fields = [ 'name', 'imagen', 'valor', 'descripcion', 'estado', 'stock']
