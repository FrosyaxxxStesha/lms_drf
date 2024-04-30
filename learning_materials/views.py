from rest_framework import viewsets, generics, filters
from learning_materials import serializers
from learning_materials import models
from django_filters import rest_framework


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = models.Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = models.Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ['method', 'lesson', 'course']
    ordering_fields = ['payment_date']
