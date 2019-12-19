
from django.db import models

# Create your models here.
class Estado(models.Model):
    name= models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class Flores(models.Model):
    name = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='flor', null=True)
    valor = models.IntegerField(default=0)
    descripcion = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    stock = models.IntegerField()
  
    def __str__(self):
        return self.name

class Registrocompra(models.Model):
    usuario = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    valor = models.IntegerField()
    cantidad = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return str(self.usuario)+' '+str(self.nombre)