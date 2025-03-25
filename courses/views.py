from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Course, Module, Lesson, UserCourse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def course_detail(request, course_id):
    course_obj = get_object_or_404(Course, id=course_id)
    context = {"course": course_obj}
    return render(request, "courses/course_detail.html", context)


@login_required
def module_detail(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lessons = module.lesson_set.filter(is_hidden=False).order_by("order")
    context = {
        "course": course,
        "modules": [module],
        "module": module,
        "lessons": lessons,
        "selected_module_id": module.id,
    }
    return render(request, "courses/module_detail.html", context)


@login_required
def lesson_detail(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
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
