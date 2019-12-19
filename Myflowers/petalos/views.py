"""este comentario es para solucionar el missing doc string..."""
from django.shortcuts import render , redirect
# importar el sistema de autentificacion
from django.contrib.auth import authenticate, logout, login as auth_login
# importar los "decorators" que permiten evitar el ingreso a una pagina
# sin estar logeado
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse 
from rest_framework import viewsets
from .models import Estado, Flores, Registrocompra  # importar el modelo
# para lograr el ingreso de usuarios regsitrados al sistema, se debe
# incorporar el modelo de usuarios registrados de Django
#from django.contrib.auth.models import User
from .forms import FloresForm
from .clase import componente
#rest_framework

from .serializers import FloresSerializer
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import HttpResponse, HttpResponseBadRequest
from fcm_django.models import FCMDevice

 
@csrf_exempt
@require_http_methods(['login'])
def guardar_token(request):
   #{token:2342334jsladfkaskj234hgakj3bs}
    body = request.body.decode('utf-8')
    bodyDict = json.loads(body)
    token = bodyDict['token']
    existe = FCMDevice.objects.filter(registratio_id = token, active=True)

    if len(existe) > 0:
        return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))

    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True

    if request.user.is_authenticated:
        dispositivo.user = request.user

    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje':' token guardado'})) 
    except :
        return HttpResponseBadRequest(json.dumps({'mensaje':' no se ha podido guardar'})) 
# Create your views here.
@login_required(login_url='/login/')
def home(request):
    """este comentario es para solucionar el missing doc string..."""
    return render(request, 'core/Home.html')
    # retorna la pagina renderizada


def cerrar_sesion(request):
    """este comentario es para solucionar el missing doc string..."""
    logout(request)
    return HttpResponse("<script>alert('cerrar sesion');window.location.href='/';</script>")


@login_required(login_url='/login/')
def agregar_carro(request, id):
    """este comentario es para solucionar el missing doc string..."""
    # recuperar una sesion llamada 'carrocompra' de no existir no deja nada ''
    sesion = request.session.get("carrocompra", "")
    # en la sesion 'carro' almaceno lo que trae la sesion mas el titulo de la flor
    request.session["carrocompra"] = sesion+str(id)+" "
    # recuperar el listado de flores
    flor = Flores.objects.all()
    msg = 'Agregar Flor'
    # renderizar la pagina,pasandole el listado de flores
    return render(request, 'core/Galeria.html', {'listaflor': flor, 'msg': msg})


@login_required(login_url='/login')
def carrocompra(request):
    """este comentario es para solucionar el missing doc string..."""
    lista = request.session.get("carrocompra", "")
    return render(request, 'core/Carrito.html', {'lista': lista})


@login_required(login_url='/login/')
def carros(request):
    x = request.session["carritox"]
    suma = 0
    for item in x:
        suma = suma+int(item["total"])
    return render(request, 'core/Carrito.html', {'x': x, 'total': suma})


@login_required(login_url='/login/')
def grabar_carro(request):
    x = request.session["carritox"]
    usr = request.user.username
    suma = 0
    try:
        for item in x:
            nombre = item["nombre"]
            valor = int(item["valor"])
            cantidad = int(item["cantidad"])
            total = int(item["total"])
            registrocompra = Registrocompra(
                usuario=usuario,
                nombre=nombre,
                valor=valor,
                cantidad=cantidad,
                total=total,

            )
            registrocompra.save()
            suma = suma+int(total)
            print("Registro Completado")
        mensaje = "Guardado"
        request.session["carritox"] = []
    except:
        mensaje = "error al guardar"
    return render(request, 'core/Carrito.html', {'x': x, 'total': suma, 'mensaje': mensaje})


@login_required(login_url='/login/')
def carro_compras(request, id):
    f = Flores.objects.get(name=id)
    x = request.session["carritox"]
    co = componente(1, f.nombre, f.valor, 1)
    sw = 0
    suma = 0
    clon = []
    for item in x:
        cantidad = item["cantidad"]
        if item["nombre"] == f.name:
            sw = 1
            cantidad = int(cantidad)+1
        co = componente(1, item["nombre"], item["valor"], cantidad)
        suma = suma+int(co.total())
        clon.append(co.toString())
    if sw == 0:
        clon.append(co.toString())
    x = clon
    request.session["carritox"] = x
    flor = Flores.objects.all()
    return render(request, 'core/Galeria.html', {'flores': flor, 'total': suma})


@login_required(login_url='/login/')
def carro_compras_mas(request, id):
    f = Flores.objects.get(name=id)
    x = request.session["carritox"]
    suma = 0
    clon = []
    for item in x:
        cantidad = item["cantidad"]
        if item["nombre"] == f.name:
            cantidad = int(cantidad)+1
        co = componente(1, item["nombre"], item["valor"], cantidad)
        suma = suma+int(co.total())
        clon.append(co.toString())
    x = clon
    request.session["carritox"] = x
    x = request.session["carritox"]
    return render(request, 'core/Carrito.html', {'x': x, 'total': suma})


@login_required(login_url='/login/')
def carro_compras_menos(request, id):
    f = Flores.objects.get(name=id)
    x = request.session["carritox"]
    total = 0
    clon = []
    suma = 0
    for item in x:
        cantidad = item["cantidad"]
        if item["nombre"] == f.name:
            cantidad = int(cantidad)-1
        co = componente(1, item["nombre"], item["valor"], cantidad)
        suma = suma+int(co.total)
        clon.append(co.toString())
    x =clon
    request.session["carritox"] = x
    x = request.session["carritox"]
    return render(request, 'core/Carrito.html', {'x': x, 'total' :total})


def login(request):
    """este comentario es para solucionar el missing doc string..."""
    if request.POST:
        usr = request.POST.get("txtUsuario")
        pwd = request.POST.get("txtPass")
        usu= authenticate(request, username=usr, password= pwd)
        mensaje = ' '
        request.session["carrito"] = []
        request.session["carritox"] = []
        print('realizado')
        if usr is not None and usr.is_active:
            auth_login(request,usr)
            return render(request, 'core/Home.html') 
        else:
            return render(request, 'core/Login.html')

    return render(request, 'core/Login.html')


def login_iniciar(request):
    """este comentario es para solucionar el missing doc string..."""
    if request.POST:
        usr = request.POST.get("txtUsuario")
        pwd = request.POST.get("txtPass")
        usu = authenticate(request, username=usr, password=pwd)
        if usu is not None and usu.is_active:
            auth_login(request, usu)
            return render(request, 'core/Home.html')
    return render(request, 'core/Login.html')


@login_required(login_url='/login/')
def eliminar_flor(request, id):
    """este comentario es para solucionar el missing doc string..."""
    mensaje = ''
    flore = Flores.objects.get(name=id)
    try:
        flore.delete()
        mensaje = 'elimino flor del catalogo'
    except:
        mensaje = 'no se puede eliminar flor del catalogo'

    flor = Flores.objects.all()  # select * from flor
    return render(request, 'core/Galeria.html', {'listaflor': flor, 'msg': mensaje})


def listar_flor(request):

    flores = Flores.objects.all()
    data = {
        'flores': flores
    }
    return render(request, 'core/listar_flores.html', data)


def modificar(request, id):
    flores = Flores.objects.get(id=id)
    data = {
        'form': FloresForm(instance=flores)
    }
    return render(request, 'core/Modificar.html', data)


@login_required(login_url='/login/')
def galeria(request):
    """este comentario es para solucionar el missing doc string..."""
    flor = Flores.objects.all()  # select * from Flores
    return render(request, 'core/Galeria.html', {'listaflor': flor})


@login_required(login_url='/login/')
def formulario2(request):
    """este comentario es para solucionar el missing doc string..."""
    estados = Estado.objects.all()  # select from Categoria
    if request.POST:
        # recupero imagen desde formulario
        imagen = request.FILES.get("txtImagen")
        nombre = request.POST.get("txtNombre")
        valor = request.POST.get("txtValor")
        descripcion = request.POST.get("txtDescripcion")
        estado = request.POST.get("cboEstado")
        # recupera el objeto con 'name' enviado desde el comboBox (cboEstado)
        obj_estado = Estado.objects.get(name=estado)
        stock = request.POST.get("txtStock")
        # Se crea una instancia de Flores(modelo)
        flores = Flores(
            imagen=imagen,
            name=nombre,
            valor=valor,
            descripcion=descripcion,
            estado=obj_estado,
            stock=stock
        )
        flores.save()  # graba objeto en bdd
        return render(request, 'core/Formulario2.html', {'lista': estados, 'msg': 'grabo', 'sw': True})
      # pasan los datos a la web
    return render(request, 'core/Formulario2.html', {'lista': estados})


@login_required(login_url='/login/')
def formulario(request):
    """este comentario es para solucionar el missing doc string..."""
    mensaje = ''
    buleano = False
    if request.POST:
        accion = request.POST.get("Accion")
        if accion == "Guardar":
            name = request.POST.get("txtEstado")
            est = Estado(
                name=name
            )
            est.save()
            mensaje = 'Grabo'
            buleano = True
        else:  # accion == "Eliminar":
            name = request.POST.get("txtEstado")
            est = Estado.objects.get(name=name)
            est.delete()
            mensaje = "Elimino"
            buleano = True
    else:
        buleano = False

    estados = Estado.objects.all()  # select * from estado
    return render(request, 'core/Formulario.html', {'lista': estados, 'msg': mensaje, 'buleano': True})

class FloresViewSet(viewsets.ModelViewSet):
    queryset = Flores.objects.all()
    serializer_class = FloresSerializer


