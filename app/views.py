from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate as auth_authenticate
from django.db import IntegrityError
from .forms import crearRegistroForm, primerRegistro
from .models import Registro

def base(request):
    if request.user.is_authenticated:
        datoregistros = Registro.objects.filter(user=request.user)
        return render(request, 'home.html', {'datoregistros': datoregistros})
    else:
        return render(request, 'home.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                auth_login(request, user)
                return redirect('principalusuarios')
            except IntegrityError:
                return render(request, 'registro.html', {'form': UserCreationForm(), 'error': 'El usuario ya existe'})
        return render(request, 'registro.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden'})

def principalusuarios(request):
    datoregistros = Registro.objects.filter(user=request.user)
    return render(request, 'principalusuarios.html', {'datoregistros': datoregistros})

def crearSaldos(request):
    if request.method == 'GET':
        return render(request, 'primerRegistro.html', {'form': primerRegistro()})
    else:
        try:
            form = primerRegistro(request.POST)
            nuevoRegistro = form.save(commit=False)
            print([nuevoRegistro.fecha, nuevoRegistro.detalle, nuevoRegistro.esaldo, nuevoRegistro.bsaldo])
            if nuevoRegistro.eingresos is None:
                nuevoRegistro.eingresos = 0.0
            if nuevoRegistro.eegresos is None:
                nuevoRegistro.eegresos = 0.0
            if nuevoRegistro.bingresos is None:
                nuevoRegistro.bingresos = 0.0
            if nuevoRegistro.begresos is None:
                nuevoRegistro.begresos = 0.0
            nuevoRegistro.user = request.user
            nuevoRegistro.save()

            return redirect('principalusuarios')
        except ValueError:
            return render(request, 'primerRegistro.html', {'form': primerRegistro(),  'error': 'Datos incorrectos'})

def crearregistro(request):
    if request.method == 'GET':
        return render(request, 'crearRegistro.html', {'form': crearRegistroForm()})
    else:
        try:
            form = crearRegistroForm(request.POST)
            nuevoRegistro = form.save(commit=False)
            print([nuevoRegistro.fecha, nuevoRegistro.detalle, nuevoRegistro.ncomprobante, nuevoRegistro.eingresos, nuevoRegistro.eegresos, nuevoRegistro.esaldo, nuevoRegistro.bingresos, nuevoRegistro.begresos, nuevoRegistro.bsaldo])
            nuevoRegistro.esaldo = Registro.objects.filter(user=request.user).last().esaldo
            if nuevoRegistro.esaldo is None:
                for i in Registro.objects.filter(user=request.user):
                    if i.esaldo is not None:
                        nuevoRegistro.esaldo = i.esaldo
                        break
            if nuevoRegistro.eingresos is not None:
                nuevoRegistro.esaldo = nuevoRegistro.esaldo + nuevoRegistro.eingresos
            else:
                nuevoRegistro.eingresos = 0.0
            if nuevoRegistro.eegresos is not None:
                nuevoRegistro.esaldo = nuevoRegistro.esaldo - nuevoRegistro.eegresos   
            else:
                nuevoRegistro.eegresos = 0.0
            nuevoRegistro.bsaldo = Registro.objects.filter(user=request.user).last().bsaldo 
            if nuevoRegistro.bsaldo is None:
                for i in Registro.objects.filter(user=request.user):
                    if i.bsaldo is not None:
                        nuevoRegistro.bsaldo = i.bsaldo
                        break
            if nuevoRegistro.bingresos is not None:
                nuevoRegistro.bsaldo = nuevoRegistro.bsaldo + nuevoRegistro.bingresos
            else:
                nuevoRegistro.bingresos = 0.0
            if nuevoRegistro.begresos is not None:
                nuevoRegistro.bsaldo = nuevoRegistro.bsaldo - nuevoRegistro.begresos
            else:
                nuevoRegistro.begresos = 0.0
            nuevoRegistro.user = request.user
            nuevoRegistro.save()

            return redirect('principalusuarios')
        except ValueError:
            return render(request, 'crearRegistro.html', {'form': crearRegistroForm(),  'error': 'Datos incorrectos'})
    
def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, 'iniciosesion.html', {'form': AuthenticationForm()})
    else:
        user = auth_authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('principalusuarios')
        else:
            return render(request, 'iniciosesion.html', {'form': AuthenticationForm(),'error': 'Usuario o contraseña incorrectos'})
    
def cerrarsesion(request):
    auth_logout(request)
    return redirect('base')
    