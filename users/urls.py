from django.urls import path
from django.contrib.auth import views

urlpatterns = [
    path('user_login/', views.LoginView.as_view(redirect_authenticated_user=True), name='user_login'),  # Вход
    path('user_logout/', views.LogoutView.as_view(), name='user_logout'),  # Выход
]
