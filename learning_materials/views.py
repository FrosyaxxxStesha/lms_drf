from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated

from learning_materials import serializers
from learning_materials import models
from django_filters import rest_framework
from learning_materials.permissions import IsModerator, IsOwner, OwnerListOnly


class CreationWithOwnerMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseViewSet(CreationWithOwnerMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwner | IsModerator]
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsModerator | OwnerListOnly]
        elif self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "delete":
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsOwner | IsModerator]
        return [permission() for permission in [IsAuthenticated] + self.permission_classes]


class LessonCreateAPIView(CreationWithOwnerMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsModerator]
    serializer_class = serializers.LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsModerator | OwnerListOnly]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = models.Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ['method', 'lesson', 'course']
    ordering_fields = ['payment_date']
