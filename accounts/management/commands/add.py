from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Module, Lesson
import random
from faker import Faker

fake = Faker('ru_RU')  # Устанавливаем локализацию на русский язык

class Command(BaseCommand):
    help = 'Добавляет данные в базу данных'

    def handle(self, *args, **kwargs):
        # Создание пользователей
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
                email=fake.email()
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь {user.username}'))

        # Создание категорий с русскими названиями
        category_titles = [
            "Программирование", "Дизайн", "Маркетинг", "Бизнес", "Наука"
        ]
        categories = []
        for i, title in enumerate(category_titles):
            category = Category.objects.create(
                title=title,
                order=i
            )
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Создана категория {category.title}'))

        # Создание курсов с русскими названиями и описаниями
        courses = []
        for i in range(10):
            course = Course.objects.create(
                title=fake.sentence(nb_words=4).rstrip('.'),
                description=fake.text(max_nb_chars=200),
                author=random.choice(users),
                category=random.choice(categories),
                date_start=fake.date_between(start_date='-1y', end_date='+1y'),
                date_stop=fake.date_between(start_date='+1y', end_date='+2y')
            )
            courses.append(course)
            self.stdout.write(self.style.SUCCESS(f'Создан курс {course.title}'))

        # Создание модулей с русскими названиями и описаниями
        modules = []
        for i in range(20):
            module = Module.objects.create(
                course=random.choice(courses),
                title=fake.sentence(nb_words=3).rstrip('.'),
                description=fake.text(max_nb_chars=150),
                author=random.choice(users),
                order=i,
                date_start=fake.date_between(start_date='-1y', end_date='+1y'),
                date_stop=fake.date_between(start_date='+1y', end_date='+2y')
            )
            modules.append(module)
            self.stdout.write(self.style.SUCCESS(f'Создан модуль {module.title}'))

        # Создание уроков с русскими названиями и содержанием
        for i in range(50):
            lesson = Lesson.objects.create(
                module=random.choice(modules),
                title=fake.sentence(nb_words=3).rstrip('.'),
                content=fake.text(max_nb_chars=300),
                video_url=fake.url(),
                description=fake.text(max_nb_chars=150),
                author=random.choice(users),
                order=i
            )
            self.stdout.write(self.style.SUCCESS(f'Создан урок {lesson.title}'))

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в базу данных'))
