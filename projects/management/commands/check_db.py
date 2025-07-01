from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check database connection'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ PostgreSQL connection successful!')
                )
                self.stdout.write(f'📊 PostgreSQL version: {result[0]}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Database connection error: {e}')
            )