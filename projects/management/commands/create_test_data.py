from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, Vacancy
from decimal import Decimal
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create test data for projects and vacancies'

    def handle(self, *args, **options):
        # Create test users
        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'testuser{i}',
                defaults={
                    'email': f'testuser{i}@example.com',
                    'first_name': f'Test{i}',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'✅ Created user: {user.username}')
            users.append(user)

        # Create test projects
        projects_data = [
            {
                'title': 'E-commerce Platform',
                'description': 'Building modern e-commerce platform with microservices architecture',
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Redis'],
                'budget': Decimal('150000.00'),
                'deadline': date.today() + timedelta(days=90),
                'owner': users[0]
            },
            {
                'title': 'Food Delivery Mobile App',
                'description': 'Developing mobile application for food delivery service',
                'technologies': ['React Native', 'Node.js', 'MongoDB', 'Socket.io'],
                'budget': Decimal('80000.00'),
                'deadline': date.today() + timedelta(days=60),
                'owner': users[1]
            },
            {
                'title': 'Data Analytics System',
                'description': 'Big Data solution for analyzing user behavior patterns',
                'technologies': ['Python', 'Apache Spark', 'Kafka', 'Elasticsearch'],
                'budget': Decimal('200000.00'),
                'deadline': date.today() + timedelta(days=120),
                'owner': users[2]
            }
        ]

        projects = []
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            if created:
                self.stdout.write(f'✅ Created project: {project.title}')
            projects.append(project)

        # Create vacancies for projects
        vacancies_data = [
            {
                'title': 'Senior Python Developer',
                'description': 'Looking for experienced Python developer to work on backend platform',
                'requirements': 'Python 3.8+, Django, PostgreSQL, 3+ years experience',
                'salary_min': Decimal('120000.00'),
                'salary_max': Decimal('180000.00'),
                'employment_type': 'full-time',
                'project': projects[0]
            },
            {
                'title': 'React Native Developer',
                'description': 'Mobile application developer with React Native expertise',
                'requirements': 'React Native, JavaScript/TypeScript, mobile development experience',
                'salary_min': Decimal('100000.00'),
                'salary_max': Decimal('150000.00'),
                'employment_type': 'full-time',
                'project': projects[1]
            },
            {
                'title': 'Data Engineer',
                'description': 'Data engineer for working with large volumes of information',
                'requirements': 'Python, Apache Spark, Kafka, Big Data experience',
                'salary_min': Decimal('140000.00'),
                'salary_max': Decimal('200000.00'),
                'employment_type': 'full-time',
                'project': projects[2]
            },
            {
                'title': 'Frontend Developer (Intern)',
                'description': 'Internship opportunity in frontend development team',
                'requirements': 'Basic knowledge of React, HTML, CSS, JavaScript',
                'salary_min': Decimal('40000.00'),
                'salary_max': Decimal('60000.00'),
                'employment_type': 'internship',
                'project': projects[0]
            }
        ]

        for vacancy_data in vacancies_data:
            vacancy, created = Vacancy.objects.get_or_create(
                title=vacancy_data['title'],
                project=vacancy_data['project'],
                defaults=vacancy_data
            )
            if created:
                self.stdout.write(f'✅ Created vacancy: {vacancy.title}')

        self.stdout.write(
            self.style.SUCCESS('🎉 Test data created successfully!')
        )
        self.stdout.write(f'📊 Projects created: {len(projects)}')
        self.stdout.write(f'👥 Vacancies created: {len(vacancies_data)}')