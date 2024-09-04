from django.contrib import admin
from django.urls import path
from .views import create_new_user, create_todo_list, update_todo_list, delete_todo
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('create-user/', create_new_user, name="create user"),
    path('create-todo/', create_todo_list, name="create todo"),
    path('update-todo/', update_todo_list, name="update todo"),
    path('delete-todo/', delete_todo, name="delete todo")
]
