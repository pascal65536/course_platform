from django.contrib import admin
from django.urls import path, include
from courses.views import course_page, user2course, user_courses
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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
