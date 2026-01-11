# -*- coding: utf-8 -*-
"""
Management command para tornar um usuário superusuário
Execute: python manage.py make_superuser rafael@chamaomika.com
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Torna um usuário superusuário pelo email ou username'

    def add_arguments(self, parser):
        parser.add_argument(
            'identifier',
            type=str,
            help='Email ou username do usuário'
        )

    def handle(self, *args, **options):
        identifier = options['identifier']
        
        # Tentar encontrar por email primeiro
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            # Se não encontrar por email, tentar por username
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuário "{identifier}" não encontrado!')
                )
                return
        
        # Tornar superusuário
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuário "{user.email}" agora é superusuário!')
        )
        self.stdout.write(f'   Username: {user.username}')
        self.stdout.write(f'   Email: {user.email}')
        self.stdout.write(f'   Superuser: {user.is_superuser}')
        self.stdout.write(f'   Staff: {user.is_staff}')




