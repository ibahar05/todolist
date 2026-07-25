from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/dashboard.html"
    context_object_name = "tasks"

    def get_queryset(self):
        task = Task.objects.filter(user=self.request.user)

        filter_type = self.request.GET.get("filter")

        if filter_type == "active":
            task = task.filter(is_completed=False)

        elif filter_type == "completed":
            task = task.filter(is_completed=True)

        return task
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(user=self.request.user)

        context["all_tasks"] = tasks.count()
        context["completed_tasks"] = tasks.filter(is_completed=True).count()
        context["pending_tasks"] = tasks.filter(is_completed=False).count()
        context["form"] = TaskForm()

        return context


class CreateTaskView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    # بعد از ساخت موفق، کاربر به صفحه اصلی دشبورد بازمی‌گردد
    success_url = reverse_lazy('todo:todo') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy("todo:todo")

class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = "tasks"
    success_url = reverse_lazy("todo:todo")

class ToggleTaskView(LoginRequiredMixin,View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_completed = not task.is_completed  
        task.save()
        
        return redirect("todo:todo")