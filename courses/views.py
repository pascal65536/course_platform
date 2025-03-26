from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Course, Module, Lesson, UserCourse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import markdown




@login_required
def course_detail(request, course_id):
    course_obj = get_object_or_404(Course, id=course_id)

    modules_list = list()
    modules_qs = Module.objects.filter(course=course_obj, is_hidden=False).order_by('order')
    for modules in modules_qs:
        modules_dct = dict()
        modules_dct.setdefault(modules.id, dict())
        modules_dct[modules.id]['module'] = modules
        modules_dct[modules.id]['lessons'] = list()
        for lesson in modules.get_lessons():
            modules_dct[modules.id]['lessons'].append(lesson)
        modules_list.append(modules_dct[modules.id])

    context = {"course": course_obj, "modules_list": modules_list}
    return render(request, "courses/course_detail.html", context)


@login_required
def module_detail(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lessons_qs = Lesson.objects.filter(module=module, is_hidden=False).order_by('order')
    context = {
        "course": course,
        "module": module,
        "lessons_qs": lessons_qs,
        "selected_module_id": module.id,
    }        
    return render(request, "courses/module_detail.html", context)


@login_required
def edit_lesson(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    if not request.user.is_staff:
        return redirect('lesson_detail', course_id=course.id, module_id=module.id, lesson_id=lesson.id)
    if request.method == 'POST':
        lesson.title = request.POST.get('title')
        lesson.description = request.POST.get('description')
        lesson.content = request.POST.get('content')
        lesson.save()
        return redirect('lesson_detail', course_id=course.id, module_id=module.id, lesson_id=lesson.id)
    return render(request, 'courses/edit_lesson.html', {'lesson': lesson})


@login_required
def lesson_detail(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    lesson.html = markdown.markdown(lesson.content, extensions=["fenced_code", "codehilite"])
    context = {
        "course": course,
        "modules": [module],
        "module": module,
        "lesson": lesson,
        "selected_module_id": module.id,
        "selected_lesson_id": lesson.id,
    }
    return render(request, "courses/lesson_detail.html", context)


def course_page(request):
    usercourse_dct = dict()
    user = request.user
    if user.is_authenticated:
        usercourse_lstdct = UserCourse.objects.filter(
            user=user, delete__isnull=True
        ).values("course_id", "rating", "progress", "is_paid", "status")
        for usercourse in usercourse_lstdct:
            usercourse_dct[usercourse["course_id"]] = usercourse

    course_lstdct = Course.objects.filter(date_stop__gte=timezone.now()).values(
        "category_id",
        "id",
        "category__title",
        "title",
        "description",
        "date_start",
        "date_stop",
        "author_id",
    )

    categories_dct = dict()
    for cat in course_lstdct:
        cat.update({"usercourse": usercourse_dct.get(cat["id"], dict())})
        categories_dct.setdefault(cat["category_id"], list())
        categories_dct[cat["category_id"]].append(cat)

    return render(
        request,
        "courses/courses.html",
        {
            "categories_dct": categories_dct,
        },
    )


@login_required
def user_courses(request):
    user = request.user
    usercourse_lstdct = (
        UserCourse.objects.filter(user=user, delete__isnull=True)
        .order_by("-created_at")
        .values(
            "course__title",
            "course__category__title",
            "course__author__username",
            "created_at",
            "completed_at",
            "last_accessed",
            "course__description",
            "rating",
            "progress",
            "is_paid",
            "status",
            "course_id",
        )
    )
    return render(
        request,
        "courses/user_courses.html",
        {
            "usercourse_lstdct": usercourse_lstdct,
        },
    )


@login_required
def user2course(request):
    if request.method == "POST":
        user = request.user
        course_id = request.POST.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        if UserCourse.objects.filter(
            user=user, course=course, delete__isnull=True
        ).exists():
            defaults = {"delete": timezone.now()}
            UserCourse.objects.update_or_create(
                user=user, course=course, defaults=defaults
            )
            messages.warning(request, "Вы покинули этот курс.")
        else:
            defaults = {"delete": None}
            UserCourse.objects.update_or_create(
                user=user, course=course, defaults=defaults
            )
            messages.success(request, "Вы успешно записаны на курс!")
        return redirect("course_page")
        # return redirect("course_detail", course_id=course_id)
    # else:
    #     return redirect("course_page")
