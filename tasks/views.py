from django.core.paginator import Paginator
from .models import Task
from django.shortcuts import render, get_object_or_404
def tasks_list(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/tasks_list.html", {
        "tasks": page_obj.object_list,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    })



def task_detail(request, task_slug):
    task = get_object_or_404(Task, slug=task_slug)
    return render(request, "tasks/task_detail.html", {"task": task})


def sound_lesson(request):
    return render(request, "tasks/sound_lesson.html")  # або "lessons/sound_lesson.html" залежно від шляху

