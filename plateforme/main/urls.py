from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('courses/<int:id>/', views.course_detail, name='course_detail'),
    path('add-youtube/', views.add_course_from_youtube, name='add_course_from_youtube'),
    path('formations/', views.formations, name='formations'),
    path('ressources/', views.ressources, name='ressources'),  # ← ajouté pour la page ressources
]
