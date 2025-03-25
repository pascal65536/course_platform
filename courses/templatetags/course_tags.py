
from django import template
from courses.models import Module, Lesson

register = template.Library()

@register.inclusion_tag('courses/left_column.html')
def render_left_column(course, selected_module_id=None, selected_lesson_id=None):
    """
    Рендерит левую колонку с модулями и уроками.
    """
    modules_list = list()
    modules_qs = Module.objects.filter(course=course, is_hidden=False).order_by('order')
    for modules in modules_qs:
        modules_dct = dict()
        modules_dct.setdefault(modules.id, dict())
        modules_dct[modules.id]['module'] = modules
        modules_dct[modules.id]['lessons'] = list()
        for lesson in modules.get_lessons():
            modules_dct[modules.id]['lessons'].append(lesson)
        modules_list.append(modules_dct[modules.id])

    context = {
        'course': course,
        'modules': modules_list,
        'selected_module_id': selected_module_id,
        'selected_lesson_id': selected_lesson_id,
    }
    return context
