from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from django.urls import path
from users import views


app_name = UsersConfig.name


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("", views.UserListAPIView.as_view(), name="list"),
    path("retrieve/<int:pk>/", views.UserRetrieveAPIView.as_view(), name="retrieve"),
    path("create/", views.UserCreateAPIView.as_view(), name="create"),
    path("update/<int:pk>/", views.UserUpdateAPIView.as_view(), name="update"),
    path("destroy/<int:pk>/", views.UserDestroyAPIView.as_view(), name="destroy"),
]
