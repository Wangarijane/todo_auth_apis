from django.urls import path

from base import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('todos/', views.TodoListCreateView.as_view(), name='todos'),
    path('todos/<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
]