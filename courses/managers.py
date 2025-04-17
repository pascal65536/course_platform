from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class CourseManager(models.Manager):
    """
    Менеджер Course
    """

    def for_user(self, user=None):
        # Базовые фильтры для дат и скрытости
        date_filter = (
            Q(date_start__isnull=True) | Q(date_start__lte=timezone.now().date())
        ) & (Q(date_stop__isnull=True) | Q(date_stop__gte=timezone.now().date()))
        hidden_filter = Q(is_hidden=False)
        author_filter = Q(author=user)

        # Определяем базовый Queryset
        qs = self.all()

        if user and user.is_superuser and user.is_active:
            return qs  # Суперпользователь видит все
        elif user and user.is_staff and user.is_active:
            return qs.filter((hidden_filter & date_filter) | author_filter)
        else:
            return qs.filter(hidden_filter & date_filter)


class UserCourseManager(models.Manager):
    """
    Менеджер UserCourse
    """

    def for_user(self, user=None):

        # Определяем базовый Queryset
        qs = self.all()
        if user and user.is_active:
            qs = qs.filter(user=user, delete__isnull=True)
            return qs
        return self.none()
