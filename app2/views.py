from django.shortcuts import render,redirect,get_object_or_404
from .formularios.registerform import NewUserForm
from .formularios.loginform import LoginForm
from .formularios import add_prov as fm
from .formularios import add_prod as fm1
from django.http import HttpResponseRedirect
from .models import Productos, Proveedores
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

# Registro de usuario.
def reg_user(request):
    if request.method == "POST":
        formulario=NewUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/")
    else:
        formulario=NewUserForm()
        return render(request,"Reg_user.html",{"form":formulario})
    
# Creamos la función donde si es administrados o estudiante.
def index(request):
    es_estudiante = request.user.groups.filter(name='Estudiante').exists()
    es_admin = request.user.is_staff
    # Si lo es tendrá acceso a las demás páginas html
    if es_estudiante or es_admin:
        return render(request, 'index.html', {'user': request.user, 'es_estudiante': es_estudiante, 'es_admin': es_admin})
    else:
        # Si no le mostrará el archivo.
        return render(request, 'sin_permiso.html')
    
# Función para iniciar sesión
def iniciar_sesion(request):
    if request.method=='POST':
        form=LoginForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

# Función para cerrar sesión.
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

@login_required(login_url=login)
def index(request):
    return render(request,'index.html',{'user':request.user})

@login_required(login_url='login')
def index(request):
    es_estudiante=request.user.groups.filter(name='Estudiante').exists()
    es_admin=request.user.is_staff
    if es_estudiante or es_admin:
        return render(request,'index.html',{'user':request.user,'es_estudiante':es_estudiante,'es_admin':es_admin})

# Archivo html para visualizar la lista de proveedores y la observaremos en una tabla.
def list_prov(request):
    proveedores = Proveedores.objects.all()
    return render(request, "lisprov.html",{'lisprov':proveedores})
# Establecemos una función para conocer si es administrador
# al intentar acceder a la url de add_prov en la terminal dirá si
# administrador junto con su usaurio si no no tendrá acceso.

def es_administrador(user):
    mostrar = user.is_authenticated and user.is_staff
    print(f"Usuario: {user.username}, ¿Es administrador?: {mostrar}")
    return mostrar

# Función para el archivo html sin_permiso
def sin_permiso(request):
    return render(request, 'sin_permiso.html')

# Usamos user_passes_test y como parámetros el nombre de la función
# del administrador, y el login /sin_permiso/ del archivo html si cumple.
# para añadir proveedores.
@user_passes_test(es_administrador,login_url='/sin_permiso/')
def add_prov(request):
    if request.method == "POST":
        formulario = fm.Add_prov(request.POST)
        if formulario.is_valid():
            nueprov=Proveedores() # Para la clase de la tabla Proveedores
            nueprov.nombre=formulario.cleaned_data["nombre"] # Se obtiene el nombre
            nueprov.telefono=formulario.cleaned_data["telefono"] # El teléfono.
            nueprov.save()
            return HttpResponseRedirect("/")
    else:
        formulario=fm.Add_prov()
    usuario_actual=request.user
    es_admin=usuario_actual.is_authenticated and usuario_actual.is_staff
    return render(request, "Add_prov.html",{"form":formulario, "es_admin":es_admin})

# Función para la lista de productos y la observaremos en una tabla.
def list_prod(request):
    productos = Productos.objects.all()
    return render(request,"lisprod.html",{'lisprod':productos})

# De igual forma utilizamos user_passes_test si cumple añadirá productos.
@user_passes_test(es_administrador,login_url='/sin_permiso/')
def add_prod(request):
    if request.method == "POST":
        formulario = fm1.Add_prod(request.POST)
        if formulario.is_valid():
            nuevprod=Productos() # Para la tabla de Produsctos.
            nuevprod.nombre=formulario.cleaned_data["nombre"] # Se obtiene el nombre
            nuevprod.stock=formulario.cleaned_data["stock"] # el stock
            fk_prov=formulario.cleaned_data["fk_prov"] # Se ocupa una varible, que se identifica en pgAdmin en nuestra tabla/campo y se recibe una llave.
            nuevprod.fk_prov=get_object_or_404(Proveedores,id=fk_prov) # Aquí se utiliza la variable de arriba ya que es una que se relaciona con id de Proveedores.
            nuevprod.save()
            return HttpResponseRedirect("/")
    else:
        formulario = fm1.Add_prod()
    usuario_actual=request.user
    es_admin=usuario_actual.is_authenticated and usuario_actual.is_staff
    return render(request,"Add_prod.html",{"form":formulario,"es_admin":es_admin})