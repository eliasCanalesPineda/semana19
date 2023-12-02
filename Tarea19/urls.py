"""
URL configuration for Tarea19 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app2 import views as ap1v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ap1v.index,name="home"),
    path('registro/',ap1v.reg_user),
    path('login/',ap1v.iniciar_sesion,name='login'),
    path('logout/',ap1v.cerrar_sesion,name='logout'),
    path('add_prov/',ap1v.add_prov,name='add_prov'),
    path('provs/',ap1v.list_prov,name='provs'),
    path('add_prod/',ap1v.add_prod,name='add_prod'),
    path('prods/',ap1v.list_prod,name='prods'),
    path('sin_permiso/',ap1v.sin_permiso,name='sin_permiso'),
]
