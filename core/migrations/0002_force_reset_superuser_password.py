from django.db import migrations
from django.contrib.auth import get_user_model

def reset_password(apps, schema_editor):
    User = get_user_model()
    # Mude 'admin' para o nome do seu superusuário, se for diferente (ex: 'jefferson')
    username_to_reset = 'jefferson' 
    
    try:
        user = User.objects.get(username=username_to_reset)
        # !!! IMPORTANTE: Defina sua nova senha aqui !!!
        new_password = 'Tecnico22@' 
        user.set_password(new_password)
        user.save()
        print(f"Senha para o usuário '{username_to_reset}' foi resetada com sucesso.")
    except User.DoesNotExist:
        print(f"Usuário '{username_to_reset}' não encontrado. Nenhuma senha foi alterada.")

class Migration(migrations.Migration):

    dependencies = [
        # Mude '0001_...' para o nome da sua última migração no app 'core'
        ('core', '0001_load_all_users'), 
    ]

    operations = [
        migrations.RunPython(reset_password),
    ]