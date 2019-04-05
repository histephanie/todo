from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Task
from django.shortcuts import render, get_object_or_404
from .forms import TaskForm

# Create your views here.
def task_list(request):
    tasks = Task.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'todo/task_detail.html', {'task' : task})

def task_new(request):
    if request.method == "TASK":
        form = TaskForm(request.TASK)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.published_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'todo/task_edit.html', {'form':form})

def task_edit(request, pk):
    task = get_object_or_404(task, pk=pk)
    if request.method == "TASK":
        form = TaskForm(request.TASK, instance=Task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.published_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=post)
    return render(request, 'todo/task_edit.html', {'form': form})
