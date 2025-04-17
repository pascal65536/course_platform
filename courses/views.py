# views.py

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Course, Module, Lesson, UserCourse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from markdown import markdown
from .forms import CourseForm, LessonForm, ModuleForm


readonly_dct = {"edit": False, "view": True, "exit": False, "append": True}
can_dct = {
    (0, 0): {"edit": False, "view": True, "exit": False, "append": True},
    (1, 0): {"edit": False, "view": True, "exit": False, "append": True},
    (1, 1): {"edit": False, "view": True, "exit": True, "append": False},
    (3, 0): {"edit": False, "view": True, "exit": False, "append": True},
    (3, 1): {"edit": False, "view": True, "exit": True, "append": False},
    (3, 2): {"edit": True, "view": False, "exit": False, "append": False},
    (7, 0): {"edit": True, "view": False, "exit": False, "append": False},
    (7, 2): {"edit": True, "view": False, "exit": False, "append": False},
    (9, 9): {"edit": False, "view": True, "exit": False, "append": True},
}


@login_required
def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.is_staff:
        return redirect("course_detail", course_id=course.id)
    form = ModuleForm()
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.author = request.user
            module.save()
            return redirect("course_detail", course_id=course.id)
    context = {"form": form, "course": course}
    return render(request, "courses/edit_module.html", context)


@login_required
def edit_module(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    if not request.user.is_staff:
        return redirect("module_detail", course_id=course.id, module_id=module.id)
    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect("module_detail", course_id=course.id, module_id=module.id)
    else:
        form = ModuleForm(instance=module)
    context = {"form": form, "module": module}
    return render(request, "courses/edit_module.html", context)


@login_required
def module_detail(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    if not module.can_view(request.user):
        return redirect("course_page")

    lessons_qs = Lesson.objects.filter(module=module, is_hidden=False).order_by("order")
    context = {
        "course": course,
        "module": module,
        "lessons_qs": lessons_qs,
        "selected_module_id": module.id,
    }
    return render(request, "courses/module_detail.html", context)


@login_required
def add_lesson(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    if not request.user.is_staff:
        return redirect("module_detail", course_id=course.id, module_id=module.id)
    form = LessonForm()
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.author = request.user
            lesson.save()
            return redirect("module_detail", course_id=course.id, module_id=module.id)
    context = {"form": form, "module": module, "course": course}
    return render(request, "courses/edit_lesson.html", context)


@login_required
def edit_lesson(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    if not request.user.is_staff:
        return redirect(
            "lesson_detail",
            course_id=course.id,
            module_id=module.id,
            lesson_id=lesson.id,
        )
    form = LessonForm(instance=lesson)
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.author = request.user
            lesson.save()
            return redirect(
                "lesson_detail",
                course_id=course.id,
                module_id=module.id,
                lesson_id=lesson.id,
            )
    context = {"form": form, "lesson": lesson}
    return render(request, "courses/edit_lesson.html", context)


@login_required
def lesson_detail(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    extensions = ["fenced_code", "codehilite", "tables"]
    lesson.html = markdown(lesson.content, extensions=extensions)
    context = {
        "course": course,
        "modules": [module],
        "module": module,
        "lesson": lesson,
        "selected_module_id": module.id,
        "selected_lesson_id": lesson.id,
    }
    return render(request, "courses/lesson_detail.html", context)


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.can_edit(request.user):
        return redirect("course_detail", course_id=course.id)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_detail", course_id=course.id)
    context = {"form": form, "course": course}
    return render(request, "courses/edit_course.html", context)


def course_page(request, *args, **kwargs):
    user = request.user
    courses_qs = Course.objects.for_user(user)
    usercourse_qs = UserCourse.objects.for_user(user)
    usercourse_qs = usercourse_qs.values_list("course_id", flat=True)
    course_list = list(usercourse_qs)
    for course in courses_qs:
        key = (
            int(user.is_active) + int(user.is_staff) * 2 + int(user.is_superuser) * 4,
            int(course.author == user) * 2 + int(course.id in course_list),
        )
        course.can = can_dct.get(key, readonly_dct)
        course.key = key
    context = {"courses_qs": courses_qs}
    return render(request, "courses/course_page.html", context=context)


@login_required
def course_detail(request, course_id):
    course_obj = get_object_or_404(Course, id=course_id)
    if not course_obj.can_view(request.user):
        return redirect("course_page")
    modules_list = list()
    modules_qs = Module.objects.filter(course=course_obj, is_hidden=False)
    modules_qs = modules_qs.order_by("order")
    for modules in modules_qs:
        modules_dct = dict()
        modules_dct.setdefault(modules.id, dict())
        modules_dct[modules.id]["module"] = modules
        modules_dct[modules.id]["lessons"] = list()
        for lesson in modules.get_lessons():
            modules_dct[modules.id]["lessons"].append(lesson)
        modules_list.append(modules_dct[modules.id])
    course_obj.editable = course_obj.can_edit(request.user)
    context = {"course": course_obj, "modules_list": modules_list}
    return render(request, "courses/course_detail.html", context)


@login_required
def user_courses(request):
    user = request.user
    usercourse_qs = UserCourse.objects.for_user(user).select_related("course", "user")
    for course in usercourse_qs:
        key = (
            int(user.is_active) + int(user.is_staff) * 2 + int(user.is_superuser) * 4,
            int(course.course.author == user) * 2 + 1,
        )
        course.can = can_dct.get(key, readonly_dct)
        course.key = key
    context = {"usercourse_qs": usercourse_qs}
    return render(request, "courses/user_courses.html", context)


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
