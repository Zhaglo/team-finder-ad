from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import User


DEFAULT_PASSWORD = 'password'


USERS = [
    {
        'email': 'maria@yandex.ru',
        'name': 'Мария',
        'surname': 'Смирнова',
        'phone': '+79000000001',
        'github_url': 'https://github.com/maria-smirnova',
        'about': 'Backend-разработчик, люблю Django и pet-проекты.',
    },
    {
        'email': 'ivan@example.com',
        'name': 'Иван',
        'surname': 'Петров',
        'phone': '+79000000002',
        'github_url': 'https://github.com/ivan-petrov',
        'about': 'Python-разработчик, интересуюсь API и автоматизацией.',
    },
    {
        'email': 'anna@example.com',
        'name': 'Анна',
        'surname': 'Кузнецова',
        'phone': '+79000000003',
        'github_url': 'https://github.com/anna-kuznetsova',
        'about': 'Frontend-разработчик, люблю React и аккуратные интерфейсы.',
    },
    {
        'email': 'oleg@example.com',
        'name': 'Олег',
        'surname': 'Морозов',
        'phone': '+79000000004',
        'github_url': 'https://github.com/oleg-morozov',
        'about': 'DevOps-энтузиаст, настраиваю Docker, CI/CD и мониторинг.',
    },
    {
        'email': 'elena@example.com',
        'name': 'Елена',
        'surname': 'Волкова',
        'phone': '+79000000005',
        'github_url': 'https://github.com/elena-volkova',
        'about': 'Дизайнер интерфейсов, помогаю pet-проектам выглядеть лучше.',
    },
]


PROJECTS = [
    {
        'owner_email': 'maria@yandex.ru',
        'name': 'TaskFlow',
        'description': 'Сервис для планирования задач небольшой команды.',
        'github_url': 'https://github.com/maria-smirnova/taskflow',
        'status': Project.Status.OPEN,
    },
    {
        'owner_email': 'ivan@example.com',
        'name': 'FoodDiary',
        'description': 'Дневник питания с подсчётом КБЖУ и простой аналитикой.',
        'github_url': 'https://github.com/ivan-petrov/fooddiary',
        'status': Project.Status.OPEN,
    },
    {
        'owner_email': 'anna@example.com',
        'name': 'Portfolio Builder',
        'description': 'Конструктор портфолио для начинающих разработчиков.',
        'github_url': 'https://github.com/anna-kuznetsova/portfolio-builder',
        'status': Project.Status.OPEN,
    },
    {
        'owner_email': 'oleg@example.com',
        'name': 'Deploy Watcher',
        'description': 'Мини-сервис для отслеживания статуса деплоев.',
        'github_url': 'https://github.com/oleg-morozov/deploy-watcher',
        'status': Project.Status.CLOSED,
    },
    {
        'owner_email': 'elena@example.com',
        'name': 'Design Review Hub',
        'description': 'Платформа для быстрой обратной связи по дизайну интерфейсов.',
        'github_url': 'https://github.com/elena-volkova/design-review-hub',
        'status': Project.Status.OPEN,
    },
]


class Command(BaseCommand):
    help = 'Create demo users, projects, participants and favorites.'

    def handle(self, *args, **options):
        users_by_email = {}

        for user_data in USERS:
            email = user_data['email']

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': user_data['name'],
                    'surname': user_data['surname'],
                    'phone': user_data['phone'],
                    'github_url': user_data['github_url'],
                    'about': user_data['about'],
                },
            )

            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
            else:
                self.stdout.write(f'User already exists: {email}')

            users_by_email[email] = user

        projects_by_name = {}

        for project_data in PROJECTS:
            owner = users_by_email[project_data['owner_email']]

            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                owner=owner,
                defaults={
                    'description': project_data['description'],
                    'github_url': project_data['github_url'],
                    'status': project_data['status'],
                },
            )

            project.participants.add(owner)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created project: {project.name}'))
            else:
                self.stdout.write(f'Project already exists: {project.name}')

            projects_by_name[project.name] = project

        # Участие в чужих проектах.
        projects_by_name['TaskFlow'].participants.add(
            users_by_email['ivan@example.com'],
            users_by_email['anna@example.com'],
        )
        projects_by_name['FoodDiary'].participants.add(
            users_by_email['maria@yandex.ru'],
            users_by_email['elena@example.com'],
        )
        projects_by_name['Portfolio Builder'].participants.add(
            users_by_email['maria@yandex.ru'],
            users_by_email['oleg@example.com'],
        )
        projects_by_name['Design Review Hub'].participants.add(
            users_by_email['anna@example.com'],
            users_by_email['ivan@example.com'],
        )

        # Избранное для проверки варианта 1.
        users_by_email['maria@yandex.ru'].favorites.add(
            projects_by_name['FoodDiary'],
            projects_by_name['Portfolio Builder'],
        )
        users_by_email['ivan@example.com'].favorites.add(
            projects_by_name['TaskFlow'],
            projects_by_name['Design Review Hub'],
        )
        users_by_email['anna@example.com'].favorites.add(
            projects_by_name['FoodDiary'],
            projects_by_name['Deploy Watcher'],
        )
        users_by_email['oleg@example.com'].favorites.add(
            projects_by_name['TaskFlow'],
        )
        users_by_email['elena@example.com'].favorites.add(
            projects_by_name['Portfolio Builder'],
            projects_by_name['TaskFlow'],
        )

        self.stdout.write(self.style.SUCCESS('Demo data created successfully.'))
        self.stdout.write('Test account: maria@yandex.ru / password')
