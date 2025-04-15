from django.contrib import admin
from django.urls import path, include
from courses.views import course_page, user2course, user_courses, course_detail, module_detail, lesson_detail, edit_lesson, edit_course, edit_module, add_module, add_lesson
from accounts.views import register, profile, custom_login, custom_logout
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', course_page, name='course_page'),
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),    
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'), 
    path('accounts/profile/', profile, name='profile'),
    path('user_courses/', user_courses, name='user_courses'),
    path('user2course/', user2course, name='user2course'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/module/<int:module_id>/', module_detail, name='module_detail'),
    path('course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/edit/', edit_lesson, name='edit_lesson'),
    path('course/<int:course_id>/edit/', edit_course, name='edit_course'),
    path('course/<int:course_id>/module/<int:module_id>/edit/', edit_module, name='edit_module'),
    path('course/<int:course_id>/module/add/', add_module, name='add_module'),
    path('course/<int:course_id>/module/<int:module_id>/lesson/add/', add_lesson, name='add_lesson'),    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path("__debug__/", include(debug_toolbar.urls)),
#     ] + urlpatterns