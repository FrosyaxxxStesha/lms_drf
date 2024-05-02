from django.contrib import admin
from learning_materials import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
