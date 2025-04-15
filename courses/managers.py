from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class CourseManager(models.Manager):
    """
    Менеджер CourseManager
    """
    def for_user(self, user=None):
        if user and user.is_superuser and user.is_active:
            qs = self.all()
        elif user and user.is_staff and user.is_active:
            qs = self.filter(Q(is_hidden=False, date_stop__gte=timezone.now()) | Q(author=user))
        else:
            qs = self.filter(is_hidden=False, date_stop__gte=timezone.now())
        return qs
