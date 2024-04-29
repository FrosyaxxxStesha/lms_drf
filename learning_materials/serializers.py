from rest_framework import serializers
from learning_materials import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'
