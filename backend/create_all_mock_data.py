# -*- coding: utf-8 -*-
"""
Script completo para criar todos os dados mockups (categorias, produtos e clientes)
Execute: python manage.py shell -c "exec(open('create_all_mock_data.py', encoding='utf-8').read())"
"""

import os
import django
import sys

# Garantir encoding UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

print("🚀 Iniciando criação de dados mockups...\n")

# Executar scripts de criação
print("=" * 50)
print("1️⃣  Criando Categorias e Produtos...")
print("=" * 50)
exec(open('create_mock_data.py', encoding='utf-8').read())

print("\n" + "=" * 50)
print("2️⃣  Criando Clientes...")
print("=" * 50)
exec(open('create_mock_clientes.py', encoding='utf-8').read())

print("\n" + "=" * 50)
print("✅ RESUMO FINAL")
print("=" * 50)

from estoque.models import Categoria, Produto
from financeiro.models import Cliente

print(f"📦 Categorias: {Categoria.objects.count()}")
print(f"👕 Produtos: {Produto.objects.count()}")
print(f"👥 Clientes: {Cliente.objects.count()}")

# Estatísticas de produtos
produtos_estoque_baixo = sum(1 for p in Produto.objects.all() if p.estoque_baixo)
print(f"⚠️  Produtos com estoque baixo: {produtos_estoque_baixo}")

print("\n🎉 Todos os dados mockups foram criados com sucesso!")
print("\n💡 Dica: Acesse o sistema e comece a testar as funcionalidades!")

