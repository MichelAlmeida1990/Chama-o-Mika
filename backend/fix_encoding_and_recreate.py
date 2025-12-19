# -*- coding: utf-8 -*-
"""
Script para corrigir encoding e recriar dados mockups
Execute: python manage.py shell -c "exec(open('fix_encoding_and_recreate.py', encoding='utf-8').read())"
"""

import os
import django
import sys

# Garantir encoding UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from estoque.models import Categoria, Produto
from financeiro.models import Cliente

print("🗑️  Limpando dados existentes...")
Produto.objects.all().delete()
Categoria.objects.all().delete()
Cliente.objects.all().delete()
print("✅ Dados limpos!\n")

print("🔄 Recriando dados com encoding UTF-8 correto...\n")

# Criar categorias
categorias_data = [
    {'nome': 'Camisetas', 'descricao': 'Camisetas básicas e estampadas'},
    {'nome': 'Calças', 'descricao': 'Calças jeans, sociais e esportivas'},
    {'nome': 'Vestidos', 'descricao': 'Vestidos casuais e sociais'},
    {'nome': 'Shorts', 'descricao': 'Shorts e bermudas'},
    {'nome': 'Blusas', 'descricao': 'Blusas e blusões'},
    {'nome': 'Saias', 'descricao': 'Saias de diversos modelos'},
    {'nome': 'Acessórios', 'descricao': 'Cintos, bolsas e acessórios'},
]

categorias = {}
for cat_data in categorias_data:
    categoria = Categoria.objects.create(
        nome=cat_data['nome'],
        descricao=cat_data['descricao']
    )
    categorias[cat_data['nome']] = categoria
    print(f"✅ Categoria criada: {cat_data['nome']}")

# Produtos de exemplo (primeiros 10 para teste)
produtos_data = [
    # Camisetas
    {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'P', 'cor': 'Branco', 'quantidade': 25, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 30, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'G', 'cor': 'Branco', 'quantidade': 20, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Básica Preta', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'P', 'cor': 'Preto', 'quantidade': 18, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Básica Preta', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 22, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Básica Preta', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'G', 'cor': 'Preto', 'quantidade': 15, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
    {'nome': 'Camiseta Estampada Azul', 'categoria': 'Camisetas', 'modelo': 'Estampada', 'tamanho': 'M', 'cor': 'Azul', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Camiseta Estampada Azul', 'categoria': 'Camisetas', 'modelo': 'Estampada', 'tamanho': 'G', 'cor': 'Azul', 'quantidade': 8, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Camiseta Polo Branca', 'categoria': 'Camisetas', 'modelo': 'Polo', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 10, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
    {'nome': 'Camiseta Polo Preta', 'categoria': 'Camisetas', 'modelo': 'Polo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 3, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
]

produtos_criados = 0
for prod_data in produtos_data:
    categoria = categorias[prod_data['categoria']]
    Produto.objects.create(
        nome=prod_data['nome'],
        categoria=categoria,
        modelo=prod_data['modelo'],
        tamanho=prod_data['tamanho'],
        cor=prod_data['cor'],
        quantidade=prod_data['quantidade'],
        quantidade_minima=prod_data['quantidade_minima'],
        preco_custo=prod_data['preco_custo'],
        preco_venda=prod_data['preco_venda'],
        ativo=True
    )
    produtos_criados += 1

print(f"\n✅ {produtos_criados} produtos criados")

# Clientes
from datetime import date

clientes_data = [
    {
        'nome': 'João Silva',
        'cpf_cnpj': '123.456.789-00',
        'email': 'joao.silva@email.com',
        'telefone': '(31) 99999-1111',
        'endereco': 'Rua das Flores, 123',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30100-000',
        'data_nascimento': date(1990, 5, 15),
        'observacoes': 'Cliente frequente, prefere produtos básicos',
        'ativo': True
    },
    {
        'nome': 'Maria Santos',
        'cpf_cnpj': '987.654.321-00',
        'email': 'maria.santos@email.com',
        'telefone': '(31) 99999-2222',
        'endereco': 'Av. Paulista, 456',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30110-000',
        'data_nascimento': date(1985, 8, 20),
        'observacoes': 'Gosta de vestidos e acessórios',
        'ativo': True
    },
]

clientes_criados = 0
for cliente_data in clientes_data:
    Cliente.objects.create(**cliente_data)
    clientes_criados += 1
    print(f"✅ Cliente criado: {cliente_data['nome']}")

print(f"\n✅ Resumo:")
print(f"   - Categorias: {Categoria.objects.count()}")
print(f"   - Produtos: {Produto.objects.count()}")
print(f"   - Clientes: {Cliente.objects.count()}")
print(f"\n🎉 Dados recriados com encoding UTF-8 correto!")


