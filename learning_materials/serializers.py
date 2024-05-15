from rest_framework import serializers
from learning_materials import validators

from learning_materials import models


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор урока
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Lesson
        fields = '__all__'
        validators = [validators.YoutubeLinkOnlyValidator(fields=["title", "description", "video_link"])]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор курса
    """
    lessons_amount = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = '__all__'
        validators = [validators.YoutubeLinkOnlyValidator(fields=["title", "description"])]

    def get_lessons_amount(self, obj):
        return obj.lesson.count()

    def get_subscription(self, obj):
        return obj.subscription.filter(user=self.context.get("request").user).exists()


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежа
    """
    class Meta:
        model = models.Payment
        fields = '__all__'
        read_only_fields = ("user", "method")
