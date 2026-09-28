from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='adminpws').exists():
        User.objects.create_superuser(
            username='adminpws',
            email='admin@pws.com',
            password='zaky12345'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'), # Sesuaikan dengan nama file migrasi terakhir di foldermu kalau beda
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]