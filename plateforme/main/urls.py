from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('courses/<int:id>/', views.course_detail, name='course_detail'),
    path('add-youtube/', views.add_course_from_youtube, name='add_course_from_youtube'),
    path('formations/', views.formations, name='formations'),
    path('ressources/', views.ressources, name='ressources'), 
    path('apprentissage/', views.apprentissage, name='apprentissage'), 
    path('contact/', views.contact, name='contact'),

    # ================= MON APPRENTISSAGE =================
    path('apprentissage/add/<int:course_id>/', views.add_to_learning, name='add_to_learning'),
    path('apprentissage/remove/<int:course_id>/', views.remove_from_learning, name='remove_from_learning'),
]
