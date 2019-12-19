"""este comentario es para solucionar el missing doc string..."""

from django.urls import path, include
#rest_framework
from rest_framework import routers
from .views import home , login, login_iniciar, formulario2, formulario , agregar_carro , carro_compras_mas, cerrar_sesion, listar_flor, carro_compras_menos, eliminar_flor, galeria, grabar_carro, modificar, carrocompra, FloresViewSet, guardar_token


router = routers.DefaultRouter()
router.register('flores', FloresViewSet) 

urlpatterns = [
    path('', home, name='HOME'),
    path('login/', login, name='LOGIN'),
    path('galeria/', galeria, name='GALERI'),
    path('formulario2/', formulario2, name='FORMULA'),
    path('eliminar_flor/<id>/', eliminar_flor, name='ELIMINAR'),
    path('login_iniciar/', login_iniciar, name='LOGIN_INICIAR'),
    path('cerrar_sesion/', cerrar_sesion, name='CERRAR'),
    path('agregar_carro/<id>/', agregar_carro, name='A_CARRO'),
    path('carrocompra/', carrocompra, name='CARRO'),
    path('formulario/', formulario, name='FORMU'),
    path('listar-flores/', listar_flor, name='listar_flores'),
    path('modificar/', modificar, name='Modificar'),
    path('carro_mas/<id>/', carro_compras_mas, name='CARRO_MAS'),
    path('carro_menos/<id>/', carro_compras_menos, name='CARRO_MENOS'),
    path('grabar_carro/', grabar_carro, name='GRABAR_CARRO'), 
    path('api/', include(router.urls)),
    path('guardar-token/', guardar_token, name='guardar_token'), 

]
