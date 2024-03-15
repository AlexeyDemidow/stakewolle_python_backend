import re

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .models import Profile
from .utils import generate_ref_code

from .serializers import UserProfileSerializerRead, UserSerializer, ProfileSerializer


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


class AllProfileInfoAPIViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Список всех пользователей с полной информацией (админ)"""

    queryset = Profile.objects.values(
        'id',
        'user__id',
        'user__username',
        'user__email',
        'ref_code',
        'ref_by',
    )
    serializer_class = UserProfileSerializerRead
    permission_classes = (IsAdminUser,)
    my_tags = ['All users/profiles info (admin)']

    @swagger_auto_schema(
        operation_summary='List of all users with profile info (admin)',
        operation_description='Show list of all users with full information(admin)'
    )
    def list(self, request, *args, **kwargs):
        return super(AllProfileInfoAPIViewSet, self).list(request, *args, **kwargs)


class AllUserAPIViewSet(viewsets.ModelViewSet):
    """Список всех пользователей (админ)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    my_tags = ['All users (admin)']

    @swagger_auto_schema(
        operation_summary='List of all users (admin)',
        operation_description='Show list of all users (admin)'
    )
    def list(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Get user by id (admin)',
        operation_description='Retrieving a user via user id (admin)'
    )
    def retrieve(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a user (admin)',
        operation_description='Creating a user with a profile (admin)'
    )
    def create(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='User update (admin)',
        operation_description='Updating user data by user id (admin)'
    )
    def update(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial user update (admin)',
        operation_description='Partial updating user data by user id (admin)'
    )
    def partial_update(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete user (admin)',
        operation_description='User deletion by user id(admin)'
    )
    def destroy(self, request, *args, **kwargs):
        return super(AllUserAPIViewSet, self).destroy(request, *args, **kwargs)


class AllProfilesAPIViewSet(viewsets.ModelViewSet):
    """Список всех профилей пользователей (админ)"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminUser,)
    my_tags = ['All profiles (admin)']

    @swagger_auto_schema(
        operation_summary='List of all profiles (admin)',
        operation_description='Show list of all profiles (admin)'
    )
    def list(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Get profiles by id (admin)',
        operation_description='Retrieving a profiles via profile id (admin)'
    )
    def retrieve(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a profile (admin)',
        operation_description='Creating a user profile (admin)'
    )
    def create(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Profile update (admin)',
        operation_description='Updating profile data by profile id (admin)'
    )
    def update(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial profile update (admin)',
        operation_description='Partial updating profile data by profile id (admin)'
    )
    def partial_update(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete profile (admin)',
        operation_description='Profile deletion by profile id(admin)'
    )
    def destroy(self, request, *args, **kwargs):
        return super(AllProfilesAPIViewSet, self).destroy(request, *args, **kwargs)


class UserAPIViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Профиль пользователя (User)"""

    def get_queryset(self):
        user = self.request.user.id
        user_profile = User.objects.filter(id=user)
        return user_profile

    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    my_tags = ['User']

    @swagger_auto_schema(
        operation_summary='Get user',
        operation_description='Retrieving a user via user id'
    )
    def retrieve(self, request, *args, **kwargs):
        return super(UserAPIViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='User update',
        operation_description='Updating user data by user id'
    )
    def update(self, request, *args, **kwargs):
        return super(UserAPIViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial user update',
        operation_description='Partial updating user data by user id'
    )
    def partial_update(self, request, *args, **kwargs):
        return super(UserAPIViewSet, self).partial_update(request, *args, **kwargs)


class ProfileAPIViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """Профиль пользователя (Profile)"""

    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    my_tags = ['Profile']

    def get_queryset(self):
        user = self.request.user.profile.id
        user_profile = Profile.objects.filter(id=user)
        return user_profile

    @swagger_auto_schema(
        operation_summary='Create/update referral code',
        operation_description='Creation or updating of a user referral code'
    )
    @action(detail=True, methods=['get'], url_path=r'create_update_ref_code')
    def create_update_ref_code(self, request, pk):
        new_ref = generate_ref_code()
        p = get_object_or_404(Profile, id=pk)
        p.ref_code = new_ref
        p.expiration_date = timezone.now() + timezone.timedelta(minutes=3)  # Задать время жизни реферальной ссылки
        send_mail(
            'Ваш новый реферальный код',
            f'{p.user.username}, ваш реферальный код - {new_ref}\n',
            'django_fitapp@mail.ru',
            [p.user.email],
            fail_silently=False,
        )
        p.save()
        return Response('Ваш новый реферальный код - ' + new_ref)

    @swagger_auto_schema(
        operation_summary='Delete referral code',
        operation_description='Deletion of user referral code'
    )
    @action(detail=True, methods=['get'], url_path=r'delete_ref_code')
    def delete_ref_code(self, request, pk):
        p = get_object_or_404(Profile, id=pk)
        p.ref_code = ''
        p.save()
        return Response('Вы удалили свой реферальный код')

    @swagger_auto_schema(
        operation_summary='User referrals',
        operation_description='Displaying user referrals'
    )
    @action(detail=True, methods=['get'], url_path=r'my_refs')
    def my_refs(self, request, pk):
        q = Profile.objects.all()
        refs = [p for p in q if p.ref_by == self.request.user]

        return Response(f'Ваши рефералы: {" ".join([i.user.username for i in refs])}')

    @swagger_auto_schema(
        operation_summary='Get profile',
        operation_description='Retrieving a user profile via profile id'
    )
    def retrieve(self, request, *args, **kwargs):
        return super(ProfileAPIViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Profile update',
        operation_description='Updating profile data by profile id'
    )
    def update(self, request, *args, **kwargs):
        return super(ProfileAPIViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial profile update',
        operation_description='Partial updating profile data by profile id'
    )
    def partial_update(self, request, *args, **kwargs):
        return super(ProfileAPIViewSet, self).partial_update(request, *args, **kwargs)


class CreateProfileAPIView(generics.CreateAPIView):
    """Создание пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    my_tags = ['Create user and profile']

    @swagger_auto_schema(
        operation_summary='Create a user',
        operation_description='Creating a user with a profile'
    )
    def post(self, request, *args, **kwargs):
        return super(CreateProfileAPIView, self).post(request, *args, **kwargs)


class CreateReferralProfileAPIView(generics.CreateAPIView):
    """Создание пользователя по реферальной ссылке"""

    serializer_class = UserSerializer
    my_tags = ['Create referral user and profile']

    def perform_create(self, serializer):
        ref_code = re.sub('http://127.0.0.1:8000/api/', '', str(self.request.build_absolute_uri())).removesuffix('/')
        profile = get_object_or_404(Profile, ref_code=ref_code)
        if profile:
            user = serializer.save()
            ref_user = User.objects.get(username=profile.user.username)
            user.profile.ref_by = ref_user
            user.save()

    @swagger_auto_schema(
        operation_summary='Create a user by referral code',
        operation_description='Creating a user with a profile by referral code'
    )
    def post(self, request, *args, **kwargs):
        return super(CreateReferralProfileAPIView, self).post(request, *args, **kwargs)
