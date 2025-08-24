from django.db import migrations
from django.core.management import call_command
import os

fixture_filename = 'users_backup.json'

def load_fixture(apps, schema_editor):
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', fixture_filename)
    if os.path.exists(fixture_path):
        print(f"Loading fixture from: {fixture_path}")
        call_command('loaddata', fixture_path)
    else:
        print(f"Fixture file not found at {fixture_path}. Skipping.")

def unload_fixture(apps, schema_editor):
    print(f"Skipping unload of fixture {fixture_filename}")

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]