from django.urls import path
from .views import tasks_list, task_detail

urlpatterns = [
    path("", tasks_list, name="tasks_list"),
    path("<slug:task_slug>/", task_detail, name="task_detail"),
]
