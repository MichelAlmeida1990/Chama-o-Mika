"""
WSGI config for gestao project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')

application = get_wsgi_application()

# Criar superusuário padrão automaticamente se não existir
# Ativado via variável de ambiente AUTO_CREATE_SUPERUSER=True
if os.environ.get('AUTO_CREATE_SUPERUSER', 'False') == 'True':
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print('✅ Superusuário padrão criado automaticamente!')
            print('   Username: admin')
            print('   Password: admin123')
    except Exception as e:
        print(f'⚠️ Erro ao criar superusuário: {e}')


