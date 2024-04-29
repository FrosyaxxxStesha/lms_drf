from django.urls import path
from rest_framework import routers
from learning_materials import views
from learning_materials.apps import LearningMaterialsConfig


app_name = LearningMaterialsConfig.name


router = routers.DefaultRouter()
router.register("course", views.CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/create/", views.LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/list/", views.LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/retrieve/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/update/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/destroy/<int:pk>/", views.LessonDestroyAPIView.as_view(), name="lesson_destroy"),

] + router.urls
