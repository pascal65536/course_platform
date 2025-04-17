from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .managers import CourseManager, UserCourseManager


class Category(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False, verbose_name="Скрыт от учеников")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def can_view(self, user):
        if not user.is_active:
            return False
        if user.is_superuser:
            return True
        if user.is_staff and user == self.author:
            return True
        if self.is_hidden:
            return False
        date_start = self.date_start or timezone.datetime.now().date()
        date_stop = self.date_stop or timezone.datetime.now().date()            
        if date_start <= timezone.now().date() <= date_stop:   
            return True
        return False


    def can_edit(self, user):
        if not user.is_active:
            return False        
        if user.is_superuser:
            return True
        if user.is_staff and user == self.author:
            return True
        return False

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False, verbose_name="Скрыт от учеников")
    created_at = models.DateTimeField(auto_now_add=True)

    def can_view(self, user):
        if not user.is_active:
            return False
        if user.is_superuser:
            return True
        if user.is_staff and user == self.author:
            return True
        if self.course not in user.course_set.all():
            return False
        if self.is_hidden:
            return False
        date_start = self.date_start or timezone.datetime.now().date()
        date_stop = self.date_stop or timezone.datetime.now().date()            
        if date_start <= timezone.now().date() <= date_stop:   
            return True
        return False

    def can_edit(self, user):
        if not user.is_active:
            return False        
        if user.is_superuser:
            return True
        if user.is_staff and user == self.author:
            return True
        return False

    def __str__(self):
        return f"{self.title}"

    def get_lessons(self):
        return self.lesson_set.order_by("order")

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False, verbose_name="Скрыт от учеников")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class UserCourse(models.Model):
    STATUS_CHOICES = [
        ("author", "Автор"),
        ("student", "Ученик"),
        ("teacher", "Преподаватель"),
        ("editor", "Редактор"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="student")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершен")
    delete = models.DateTimeField(null=True, blank=True, verbose_name="Удалён")
    last_accessed = models.DateTimeField(auto_now=True, verbose_name="Последний доступ")
    progress = models.PositiveIntegerField(default=0, verbose_name="Прогресс (%)")
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Оценка курса (1-5)",
        validators=[
            MinValueValidator(1, message="Оценка должна быть не меньше 1."),
            MaxValueValidator(5, message="Оценка должна быть не больше 5."),
        ],
    )
    notes = models.TextField(blank=True, verbose_name="Заметки пользователя")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserCourseManager()

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    class Meta:
        unique_together = (
            "user",
            "course",
        )
        verbose_name = "Пользовательский курс"
        verbose_name_plural = "Пользовательские курсы"


# class Quiz(models.Model):
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateTimeField()

# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     text = models.TextField()
#     question_type = models.CharField(max_length=50)  # Например, "multiple_choice", "text"

# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)

# class Submission(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     score = models.FloatField(null=True, blank=True)
