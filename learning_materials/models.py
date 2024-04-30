from django.db import models

NULL = {
    "null": True,
    "blank": True,
}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    preview = models.ImageField(upload_to="learning_materials/course/preview/",
                                default="learning_materials/course/preview/default/course.svg",
                                verbose_name="превью фото",
                                )
    description = models.TextField(verbose_name="описание")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="learning_materials/lesson/preview/",
                                default="learning_materials/lesson/preview/default/lesson.svg",
                                verbose_name="превью фото",
                                )
    video_link = models.URLField(verbose_name="ссылка на видео", **NULL)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
