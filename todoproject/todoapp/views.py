from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic import ListView

from .forms import TaskForms
from .models import Task
# Create your views here.


class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
class Taskdetailview(DetailView):
    model= Task
    template_name = 'detail.html'
    context_object_name = 'task'

class Taskupdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'desc', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail', kwargs={'pk': self.object.id})

class Taskdeleteview(DeleteView):
    model=Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')

def home(requests):
    return render(requests,'home.html')

def add_task(requests):
    tasks = Task.objects.all()
    if requests.method == "POST":
        name = requests.POST.get('task','')
        desc = requests.POST.get('desc','')
        priority = requests.POST.get('priority','')
        date =requests.POST.get('date','')
        task = Task(name=name,desc=desc,priority=priority,date=date)
        task.save()
    return render(requests,'home.html',{'tasks':tasks})

def delete(requests, id):
    if requests.method == "POST":
        task=Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(requests,'delete.html')

def update(requests, taskid):
    task=Task.objects.get(id=taskid)
    form = TaskForms(requests.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(requests,'update.html',{'form':form,'task':task})