from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Проверка подключения к базе данных'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Подключение к PostgreSQL успешно!')
                )
                self.stdout.write(f'📊 Версия PostgreSQL: {result[0]}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка подключения к БД: {e}')
            )