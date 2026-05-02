from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('update/<int:id>/', views.update_student, name='update'),
    path('delete/<int:id>/', views.delete_student, name='delete'),
]