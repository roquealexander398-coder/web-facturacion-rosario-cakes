from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Crear usuario administrador"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123",
                role="ADMIN"
            )
            self.stdout.write(self.style.SUCCESS("Administrador creado"))
        else:
            self.stdout.write(self.style.WARNING("El administrador ya existe"))