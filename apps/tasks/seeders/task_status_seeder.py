from apps.tasks.models.status import Status

def run():
    Status.objects.create(
        name='Pendiente',
        description='Tarea pendiente por realizar'
    )
    Status.objects.create(
        name='En Progreso',
        description='Tarea en progreso'
    )
    Status.objects.create(
        name='Completada',
        description='Tarea completada'
    )