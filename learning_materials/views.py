from rest_framework import viewsets, generics, filters, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import response

from learning_materials import serializers, models
from django_filters import rest_framework

from learning_materials.permissions import IsModerator, IsOwner, OwnerListOnly


class CreationWithOwnerMixin:
    """
    Миксин для автоматического добавления пользователя при
    создании нового объекта
    """
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseViewSet(CreationWithOwnerMixin, viewsets.ModelViewSet):
    """
    Viewset, реализующий crud для модели курса
    """
    permission_classes = [IsOwner | IsModerator]
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all().prefetch_related("subscription")

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsModerator | OwnerListOnly]
        elif self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsOwner | IsModerator]
        return [permission() for permission in [IsAuthenticated] + self.permission_classes]


class LessonCreateAPIView(CreationWithOwnerMixin, generics.CreateAPIView):
    """
    Создание урока
    """
    permission_classes = [IsAuthenticated, ~IsModerator]
    serializer_class = serializers.LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """
    Просмотр списка уроков
    """
    permission_classes = [IsAuthenticated, IsModerator | OwnerListOnly]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получение одного урока
    """
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование урока
    """
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока
    """
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = models.Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """
    Просмотр списка платежей за курс или урок
    """
    permission_classes = [IsAuthenticated]
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ['method', 'lesson', 'course']
    ordering_fields = ['payment_date']


class SubscriptionAlterAPIView(views.APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(models.Course.objects.filter(pk=self.request.data.get("course")))
        subscription_data = {
            "user": user,
            "course": course
        }

        is_subscribed = models.Subscription.objects.filter(**subscription_data).exists()

        if is_subscribed:
            models.Subscription.objects.get(**subscription_data).delete()
            message = "unsubscribed"
        else:
            models.Subscription.objects.create(**subscription_data)
            message = "subscribed"

        return response.Response({"message": message})
