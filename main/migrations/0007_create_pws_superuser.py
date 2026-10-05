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
        ('main', '0006_alter_experience_id'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
