from django.db import migrations
from django.core.management import call_command
import os

# O nome do arquivo que geramos com o dumpdata
fixture_filename = 'users.json' 

def load_fixture(apps, schema_editor):
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', fixture_filename)
    if os.path.exists(fixture_path):
        # MENSAGEM IMPORTANTE PARA PROCURAR NOS LOGS DO DEPLOY
        print(f"\n\n!!! CARREGANDO FIXTURE: {fixture_path} !!!\n\n")
        call_command('loaddata', fixture_path)
    else:
        print(f"\n\n!!! ARQUIVO DE FIXTURE NÃO ENCONTRADO: {fixture_path} !!!\n\n")

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.RunPython(load_fixture),
    ]