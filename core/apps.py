from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # Este método é executado uma vez quando o Django inicia
    def ready(self):
        # Tenta importar o modelo de usuário. Se falhar (durante o setup inicial), ignora.
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            # === DEFINA SEU USUÁRIO DE EMERGÊNCIA AQUI ===
            username = 'admin_emergencia'
            password = 'SenhaDeEmergencia12345!'
            email = 'emergencia@aureon.com'
            # ============================================

            # Verifica se o usuário já existe
            if not User.objects.filter(username=username).exists():
                # Mensagem de log para procurarmos no Render
                print("\n\n" + "="*50)
                print(f"EXECUTANDO CRIAÇÃO DE SUPERUSUÁRIO DE EMERGÊNCIA: {username}")
                print("="*50 + "\n\n")
                
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
        except Exception as e:
            # Se algo der errado (ex: o banco de dados ainda não existe), apenas informa.
            print(f"AVISO: Falha ao tentar criar superusuário de emergência: {e}")