# core/management/commands/create_initial_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Cria um superusuário inicial se nenhum existir'

    def handle(self, *args, **options):
        if Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Um superusuário já existe. Nenhuma ação foi tomada.'))
            return

        # --- PERSONALIZE SEU SUPERUSUÁRIO AQUI ---
        username = 'admin'
        email = 'admin@exemplo.com'
        password = 'Maya24@@' # Use uma senha forte temporária
        # ----------------------------------------

        self.stdout.write(f"Criando superusuário inicial: {username}")
        Usuario.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!'))