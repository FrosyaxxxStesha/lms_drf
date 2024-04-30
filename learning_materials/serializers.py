from rest_framework import serializers
from learning_materials import models


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)

    class Meta:
        model = models.Course
        fields = '__all__'

    def get_lessons_amount(self, obj):
        return obj.lesson.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = '__all__'
