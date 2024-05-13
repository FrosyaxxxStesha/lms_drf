from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from learning_materials import models, views
from enum import Enum
from django.contrib.auth import get_user_model

User = get_user_model()


class LessonViewnames(str, Enum):
    create = "learning_materials:lesson_create"
    retrieve = "learning_materials:lesson_retrieve"
    retrieve_list = "learning_materials:lesson_list"
    update = "learning_materials:lesson_update"
    destroy = "learning_materials:lesson_destroy"


class SubscribeViewnames(str, Enum):
    alter = "learning_materials:subscription_alter"


class LessonAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User(email="test@mail.com")
        cls.user.set_password("1234")
        cls.user.save()

        cls.course = models.Course.objects.create(title="test", description="test_description", user=cls.user)
        cls.lesson = models.Lesson.objects.create(title="test",
                                                   description="test_description",
                                                   user=cls.user,
                                                   course=cls.course
                                                   )
        cls.viewnames = LessonViewnames

        cls.factory = APIRequestFactory()

    def test_create(self):
        data = {"title": "test",
                "description": "test_create",
                "course": 1}
        request = self.factory.post(reverse(self.viewnames.create), data, format="json")
        view = views.LessonCreateAPIView.as_view()

        force_authenticate(request, self.user)

        response = view(request)

        self.assertEqual(
            response.data,
            {
                "id": 2,
                "title": "test",
                "description": "test_create",
                "course": 1,
                "preview": "http://testserver/media/learning_materials/lesson/preview/default/lesson.svg",
                "video_link": None
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            models.Lesson.objects.filter(pk=2).exists()
        )

    def test_retrieve(self):
        request = self.factory.get(reverse(self.viewnames.retrieve, kwargs={"pk": 1}), format="json")
        view = views.LessonRetrieveAPIView.as_view()

        force_authenticate(request, self.user)

        response = view(request, pk=1)

        self.assertEqual(
            response.data,
            {
                "id": 1,
                "title": "test",
                "description": "test_description",
                "course": 1,
                "preview": "http://testserver/media/learning_materials/lesson/preview/default/lesson.svg",
                "video_link": None
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_retrieve_list(self):
        right_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "title": "test",
                    "description": "test_description",
                    "course": 1,
                    "preview": "http://testserver/media/learning_materials/lesson/preview/default/lesson.svg",
                    "video_link": None
                }
            ]
        }

        request = self.factory.get(reverse(self.viewnames.retrieve_list), format="json")
        view = views.LessonListAPIView.as_view()

        force_authenticate(request, self.user)

        response = view(request)

        self.assertEqual(
            response.data,
            right_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update(self):
        request = self.factory.patch(reverse(self.viewnames.update,
                                             kwargs={"pk": 1}),
                                     data={"description": "updated"},
                                     format="json")
        view = views.LessonUpdateAPIView.as_view()

        force_authenticate(request, self.user)

        response = view(request, pk=1)

        self.assertEqual(
            response.data,
            {
                "id": 1,
                "title": "test",
                "description": "updated",
                "course": 1,
                "preview": "http://testserver/media/learning_materials/lesson/preview/default/lesson.svg",
                "video_link": None
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete(self):
        request = self.factory.delete(reverse(self.viewnames.destroy, kwargs={"pk": 1}), format="json")
        view = views.LessonDestroyAPIView.as_view()

        force_authenticate(request, self.user)

        response = view(request, pk=1)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(email="test@mail.com")
        cls.user.set_password("1234")
        cls.user.save()

        cls.subscriber = User(email="subscriber@mail.com")
        cls.subscriber.set_password("1234")
        cls.subscriber.save()

        cls.viewnames = SubscribeViewnames

        cls.course = models.Course.objects.create(title="test", description="test_description", user=cls.user)

        cls.factory = APIRequestFactory()

    def test_alter(self):

        data = {"course": 2}
        request = self.factory.post(reverse(self.viewnames.alter), data=data, format="json")
        view = views.SubscriptionAlterAPIView.as_view()

        force_authenticate(request, self.subscriber)

        response = view(request)

        self.assertEqual(
            response.data,
            {"message": "subscribed"}
        )

        data = {"course": 2}

        request = self.factory.post(reverse(self.viewnames.alter), data=data, format="json")
        force_authenticate(request, self.subscriber)
        response = view(request)

        self.assertEqual(
            response.data,
            {"message": "unsubscribed"}
        )
