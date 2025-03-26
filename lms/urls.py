from django.contrib import admin
from django.urls import path, include
from courses.views import course_page, user2course, user_courses, course_detail, module_detail, lesson_detail, edit_lesson
from accounts.views import register, profile, custom_login, custom_logout
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
