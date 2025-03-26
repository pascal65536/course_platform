# templatetags/course_tags.py

from django import template
from courses.models import Module, Lesson

register = template.Library()

@register.inclusion_tag("courses/left_column.html", takes_context=True)
def render_left_column(context, course, selected_module_id=None, selected_lesson_id=None):
    """
    Рендерит левую колонку с модулями и уроками.
    """
    # Получаем объект user из контекста
    user = context['user']

    modules_list = []
    modules_qs = Module.objects.filter(course=course, is_hidden=False).order_by("order")
    for module in modules_qs:
        module_dict = {
            "module": module,
            "lessons": list(module.get_lessons())
        }
        modules_list.append(module_dict)

    context = {
        "course": course,
        "modules": modules_list,
        "selected_module_id": selected_module_id,
        "selected_lesson_id": selected_lesson_id,
        "user": user,  # Добавляем объект user в контекст
    }
    return context
