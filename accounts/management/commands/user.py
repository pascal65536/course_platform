from django.core.management import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


# python manage.py user
class Command(BaseCommand):

    def handle(self, *args, **options):
        print('-' * 50)

        # Создание нового пользователя
        user = User.objects.create_user(username='john', password='password123')

        # Доступ к профилю
        profile = user.profile
        profile.bio = "Hello, I'm John!"
        profile.location = "New York"
        profile.save()
        