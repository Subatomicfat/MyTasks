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
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')
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
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao MyTasks.')
            return redirect('dashboard')
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

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'task_form.html', {'form': form, 'title': 'Nova Tarefa'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'task_form.html', {'form': form, 'title': 'Editar Tarefa'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarefa excluída com sucesso!')
        return redirect('dashboard')
    
    return render(request, 'task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    
    status = "concluída" if task.completed else "pendente"
    messages.success(request, f'Tarefa marcada como {status}!')
    return redirect('dashboard')