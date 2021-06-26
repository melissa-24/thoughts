from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('thoughts/', views.dashboard),
    path('createThought/', views.createThought),
    path('thought/<int:thought_id>/',views.viewThought),
    path('thought/<int:thought_id>/editThought/', views.editThought),
    path('thought/<int:thought_id>/edit/', views.updateThought),
    path('thought/<int:thought_id>/delete/', views.deleteThought),
    path('thought/<int:thought_id>/like/', views.likeThought),
]