from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, filters, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import response

from learning_materials import serializers, models, paginators
from django_filters import rest_framework

from learning_materials.permissions import IsModerator, IsOwner, OwnerListOnly
from learning_materials.services import create_product, create_price, create_session


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
    pagination_class = paginators.CoursePaginator

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
    pagination_class = paginators.LessonPaginator


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


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, method="перевод на карту")
        product = create_product(payment.course)
        price = create_price(product=product, amount=payment.amount)
        session_id, session_url = create_session(price)
        payment.session_id = session_id
        payment.payment_link = session_url
        payment.save()


class SubscriptionAlterAPIView(views.APIView):
    """
    Подписка или отписка на курс для текущего авторизованного пользователя
    (переключает статус: если пользователь был подписан на курс до запроса - отписывает его,
    если не был подписан - подписывает)
    """
    @swagger_auto_schema(
        responses={200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="response message, can contain \"subscribed\" or \"unsubscribed\"",
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="string of response message",
                        example="subscribed"
                    )
                }

            )
        },
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, description='course for altering subscription status',
                properties={
                    'course': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='course for subscription / unsubscription id',
                        example="1"
                    ),
                }
            ),

    )
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
