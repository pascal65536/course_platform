# forms.py

from django import forms
from .models import Module, Course, Lesson


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            "title",
            "description",
            "date_start",
            "date_stop",
            "is_hidden",
            "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "date_start": forms.TextInput(
                attrs={"class": "form-control", "id": "id_date_start"}
            ),
            "date_stop": forms.TextInput(
                attrs={"class": "form-control", "id": "id_date_stop"}
            ),
            "is_hidden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Название модуля",
            "description": "Описание модуля",
            "date_start": "Дата начала",
            "date_stop": "Дата окончания",
            "is_hidden": "Скрыть от учеников",
            "order": "Порядок",
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "content", "video_url", "is_hidden", "order"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
            "is_hidden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Название урока",
            "description": "Описание урока",
            "content": "Содержимое урока",
            "video_url": "Ссылка на видео",
            "is_hidden": "Скрыть от учеников",
            "order": "Порядок",
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "author",
            "category",
            "date_start",
            "date_stop",
            "is_hidden",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "date_start": forms.TextInput(
                attrs={"class": "form-control", "id": "id_date_start"}
            ),
            "date_stop": forms.TextInput(
                attrs={"class": "form-control", "id": "id_date_stop"}
            ),
            "is_hidden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Название курса",
            "description": "Описание курса",
            "author": "Автор",
            "category": "Категория",
            "date_start": "Дата начала",
            "date_stop": "Дата окончания",
            "is_hidden": "Скрыть курс",
        }
