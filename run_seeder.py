import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.tasks.seeders.task_status_seeder import run

if __name__ == '__main__':
    run()
