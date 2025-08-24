from django.db import migrations
from django.contrib.auth import get_user_model

# ==============================================================================
# === PERSONALIZE AQUI ===
# ==============================================================================

# Coloque o nome de usuário EXATO que você quer resetar
USERNAME_PARA_RESETAR = 'teste'

# Defina a NOVA SENHA DEFINITIVA aqui. Use algo novo e forte.
NOVA_SENHA_DEFINITIVA = 'AureonVaiFuncionarAgora123!'

# ==============================================================================

def force_set_password(apps, schema_editor):
    User = get_user_model()
    try:
        print(f"\n\n!!! TENTANDO FORÇAR A SENHA PARA O USUÁRIO: {USERNAME_PARA_RESETAR} !!!")
        user = User.objects.get(username=USERNAME_PARA_RESETAR)
        user.set_password(NOVA_SENHA_DEFINITIVA)
        user.save()
        print(f"!!! SUCESSO: Senha para '{USERNAME_PARA_RESETAR}' foi forçada e salva. !!!\n\n")
    except User.DoesNotExist:
        print(f"!!! ERRO: Usuário '{USERNAME_PARA_RESETAR}' não foi encontrado no banco de dados. !!!\n\n")


class Migration(migrations.Migration):

    dependencies = [
        # MUDE '0004_...' para o nome da sua ÚLTIMA migração no app 'core'
        ('core', '0004_load_production_users'),
    ]

    operations = [
        migrations.RunPython(force_set_password),
    ]