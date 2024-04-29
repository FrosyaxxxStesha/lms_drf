from rest_framework import viewsets, generics
from learning_materials import serializers
from learning_materials import models


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
