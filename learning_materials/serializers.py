from rest_framework import serializers
from learning_materials import models


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = '__all__'

    def get_lessons_amount(self, obj):
        return obj.lesson.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'
