from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm, TaskForm
from .models import Task

# =============== VIEWS DE AUTENTICAÇÃO ===============

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}! Você está logado.')
            return redirect('dashboard')  # Redirecionamento CORRETO para o dashboard
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Login automático após registro
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao MyTasks.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('home')

# =============== VIEWS DE TAREFAS ===============

@login_required
def dashboard(request):
    # Obtém todas as tarefas do usuário logado
    tasks = Task.objects.filter(user=request.user)
    
    # Filtros
    filter_by = request.GET.get('filter')
    if filter_by == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_by == 'pending':
        tasks = tasks.filter(completed=False)
    
    # Ordenação
    order_by = request.GET.get('order', '-created_at')
    valid_orders = ['created_at', '-created_at', 'due_date', '-due_date', 'title', '-title']
    if order_by in valid_orders:
        tasks = tasks.order_by(order_by)
    
    context = {
        'tasks': tasks,
        'filter': filter_by,
        'order': order_by,
    }
    return render(request, 'dashboard.html', context)

# ... (restante das views permanece igual)
