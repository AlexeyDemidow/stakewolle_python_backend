from rest_framework import routers

from .views import AllProfileInfoAPIViewSet, AllUserAPIViewSet, AllProfilesAPIViewSet, UserAPIViewSet, ProfileAPIViewSet


# Роутер взаимодействия админа с профилями пользователей
admin_profiles_info_router = routers.SimpleRouter()
admin_profiles_info_router.register(r'admin_profiles_info', AllProfileInfoAPIViewSet)

admin_users_edit_router = routers.SimpleRouter()
admin_users_edit_router.register(r'admin_users_edit', AllUserAPIViewSet)

admin_profiles_edit_router = routers.SimpleRouter()
admin_profiles_edit_router.register(r'admin_profiles_edit', AllProfilesAPIViewSet)

user_edit_router = routers.SimpleRouter()
user_edit_router.register(r'user_edit', UserAPIViewSet, basename='user')

profile_edit_router = routers.SimpleRouter()
profile_edit_router.register(r'profile_edit', ProfileAPIViewSet, basename='profile')
