# -*- coding: utf-8 -*-
"""
Script para redefinir senha de um usuário
Execute: python reset_password.py rafael@chamaomika.com nova_senha
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if len(sys.argv) < 3:
    print("Uso: python reset_password.py <email> <nova_senha>")
    print("Exemplo: python reset_password.py rafael@chamaomika.com MinhaNovaSenha123")
    sys.exit(1)

email = sys.argv[1]
new_password = sys.argv[2]

try:
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.save()
    print(f"✅ Senha redefinida com sucesso para {email}!")
    print(f"   Nova senha: {new_password}")
except User.DoesNotExist:
    print(f"❌ Usuário com email '{email}' não encontrado!")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro ao redefinir senha: {e}")
    sys.exit(1)


