# -*- coding: utf-8 -*-
"""
Management command para criar superusuário padrão
Execute: python manage.py create_default_superuser
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria um superusuário padrão se não existir'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superusuário "{username}" já existe!')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superusuário criado com sucesso!')
            )
            self.stdout.write(f'   Username: {username}')
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Password: {password}')

