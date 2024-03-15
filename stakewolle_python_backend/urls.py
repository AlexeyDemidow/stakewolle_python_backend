from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from users.JWT_Views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView, DecoratedTokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.routers import admin_profiles_info_router, admin_users_edit_router, admin_profiles_edit_router, \
    user_edit_router, profile_edit_router
from users.views import CreateProfileAPIView, CreateReferralProfileAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Referral API",
      default_version='v1',
      description="A simple RESTful API service for a referral system.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('api/api-auth/', include('rest_framework.urls')),  # Авторизация на основе сессий cookies
    path('auth/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Авторизация JWT
    path('auth/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),

    path('api/', include(admin_profiles_info_router.urls)),  # Информация о пользователе и профиле (админ)
    path('api/', include(admin_users_edit_router.urls)),  # Работа с пользователем (админ)
    path('api/', include(admin_profiles_edit_router.urls)),  # Работа с профилем (админ)
    path('api/', include(user_edit_router.urls)),  # Работа с пользователем
    path('api/', include(profile_edit_router.urls)),  # Работа с профилем

    path('api/create_profile/', CreateProfileAPIView.as_view()),  # Создание пользователя
    path('api/<str:ref_code>/', CreateReferralProfileAPIView.as_view()),  # Создание пользователя реферальной ссылкой

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # UI документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
