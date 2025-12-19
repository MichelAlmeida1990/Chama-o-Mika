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

# Tornar usuário específico superusuário automaticamente
# Ativado via variável de ambiente MAKE_SUPERUSER=email@example.com
make_superuser_email = os.environ.get('MAKE_SUPERUSER', '').strip()
if make_superuser_email:
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email=make_superuser_email)
            if not user.is_superuser:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print(f'✅ Usuário "{make_superuser_email}" agora é superusuário!')
            else:
                print(f'ℹ️ Usuário "{make_superuser_email}" já é superusuário.')
        except User.DoesNotExist:
            print(f'⚠️ Usuário com email "{make_superuser_email}" não encontrado.')
    except Exception as e:
        print(f'⚠️ Erro ao tornar usuário superusuário: {e}')


