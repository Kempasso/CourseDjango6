from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import pagination, viewsets
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Comment
from ads.pirmissions import AuthorOrAdminPermission
from ads.serializers import AdSerializer, AdMeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


@extend_schema_view(
    list=extend_schema(description='Получение всех объявлений', summary='Объявления'),
    retrieve=extend_schema(description='Получение объявления по id', summary='Объявление'),
    create=extend_schema(description='Создание объявления', summary='Объявление'),
    destroy=extend_schema(description='Удаление объявления', summary='Объявление'),
    partial_update=extend_schema(description='Редактирование объявления', summary='Объявление'),
    update=extend_schema(description='Редактирование объявления', summary='Объявление')
)
class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        return serializer.save(author_id=self.request.user.pk)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'update', 'destroy']:
            permission_classes = [AuthorOrAdminPermission]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    serializer_class = AdSerializer


@extend_schema_view(
    list=extend_schema(description='Получение всех объявлений пользователя', summary='Объявления пользователя'),
    retrieve=extend_schema(description='Получение объявления пользователя по id', summary='Объявление пользователя'),
    create=extend_schema(description='Создание объявления', summary='Объявление пользователя'),
    destroy=extend_schema(description='Удаление объявления пользователя', summary='Объявление пользователя'),
    partial_update=extend_schema(description='Редактирование объявления пользователя', summary='Объявление пользователя'),
    update=extend_schema(description='Редактирование объявления пользователя', summary='Объявление пользователя')
)
class AdMeAPIView(viewsets.ModelViewSet):
    """Получение и редактирование объявлений пользователя"""

    def get_queryset(self):
        author = self.request.user.pk
        return Ad.objects.prefetch_related('author').filter(author_id=author).order_by('title')

    def perform_create(self, serializer):
        return serializer.save(author_id=self.request.user.pk)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'partial_update', 'update, retrieve', 'destroy']:
            permission_classes = [AuthorOrAdminPermission]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    serializer_class = AdMeSerializer


@extend_schema_view(
    list=extend_schema(description='Список всех отзывов к объявлению', summary='Отзывы объявления'),
    retrieve=extend_schema(description='Получение отзыва объявления по id', summary='Отзыв объявления'),
    create=extend_schema(description='Создание отзыва к объявлению', summary='Отзыв объявления'),
    destroy=extend_schema(description='Удаление отзыва к объявлению', summary='Отзыв объявления'),
    partial_update=extend_schema(description='Редактирование отзыва к объявлению', summary='Отзыв объявления'),
    update=extend_schema(description='Редактирование отзыва к объявлению', summary='Отзыв объявления')
)
class CommentViewSet(viewsets.ModelViewSet):
    """Создание и редактирование комментария к объявлению"""

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_pk")
        return Comment.objects.select_related('author', 'ad').filter(ad_id=ad_id).order_by('-created_at')

    def perform_create(self, serializer):
        return serializer.save(author_id=self.request.user.pk, ad_id=self.kwargs.get("ad_pk"))

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'update, retrieve', 'destroy']:
            permission_classes = [AuthorOrAdminPermission]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    serializer_class = CommentSerializer
