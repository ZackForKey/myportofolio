"""
WSGI config for myportofolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portofolio.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    from django.contrib.auth.models import User

    # Paksa jalankan migrasi database saat Gunicorn PWS baru nyala
    call_command('migrate', interactive=False)

    # Buat superuser jika belum ada
    if not User.objects.filter(username="adminpws").exists():
        User.objects.create_superuser("adminpws", "admin@pws.com", "zaky12345")
        print("Superuser adminpws berhasil dibuat di PWS!")
except Exception as e:
    print("Auto startup migration error:", e)
