# encyclopedia/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de índice
    path('search/', views.search, name='search'),  # Búsqueda
    path('random/', views.random_entry, name='random_entry'),  # Página aleatoria
    path('<str:title>/', views.entry, name='entry'),  # Página de entrada específica
    path('create/', views.create_entry, name='create_entry'),  # Crear una entrada
    path('<str:title>/edit/', views.edit_entry, name='edit_entry'),  # Editar una entrada
]