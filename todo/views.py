from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Task
from django.shortcuts import render, get_object_or_404
from .forms import TaskForm

# Create your views here.
def task_list(request):
    tasks = Task.objects.order_by('created_date')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'todo/task_detail.html', {'task' : task})

def task_new(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'todo/task_edit.html', {'form':form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not task.author == request.user:
        return "unauthorized" 

    if request.method == "POST":
        if 'delete' in request.POST:
            task.delete()
            return redirect("task_list")
        
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_edit.html', {'form': form})
