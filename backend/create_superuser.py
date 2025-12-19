import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Cria superusuário se não existir
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superusuário criado com sucesso!')
    print(f'Username: {username}')
    print(f'Password: {password}')
else:
    print(f'Superusuário "{username}" já existe!')


