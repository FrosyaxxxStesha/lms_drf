from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    Сериализатор пользователя
    """
    class Meta:
        model = User
        fields = '__all__'
