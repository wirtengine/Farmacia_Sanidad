from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .forms import RegistroForm  # Vamos a crear este formulario

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirige al home después del registro
    else:
        form = RegistroForm()
    return render(request, 'usuarios/register.html', {'form': form})