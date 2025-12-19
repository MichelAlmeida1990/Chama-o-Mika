# -*- coding: utf-8 -*-
"""
Script para criar clientes mockups
Execute: python manage.py shell -c "exec(open('create_mock_clientes.py', encoding='utf-8').read())"
"""

import os
import django
import sys

# Garantir encoding UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from financeiro.models import Cliente

# Limpar clientes existentes (opcional)
# Cliente.objects.all().delete()

# Clientes de exemplo
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
    {
        'nome': 'Pedro Oliveira',
        'cpf_cnpj': '456.789.123-00',
        'email': 'pedro.oliveira@email.com',
        'telefone': '(31) 99999-3333',
        'endereco': 'Rua do Comércio, 789',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30120-000',
        'data_nascimento': date(1992, 3, 10),
        'observacoes': 'Compra principalmente calças e camisetas',
        'ativo': True
    },
    {
        'nome': 'Ana Costa',
        'cpf_cnpj': '789.123.456-00',
        'email': 'ana.costa@email.com',
        'telefone': '(31) 99999-4444',
        'endereco': 'Rua das Palmeiras, 321',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30130-000',
        'data_nascimento': date(1988, 11, 25),
        'observacoes': 'Cliente VIP, sempre busca novidades',
        'ativo': True
    },
    {
        'nome': 'Carlos Ferreira',
        'cpf_cnpj': '321.654.987-00',
        'email': 'carlos.ferreira@email.com',
        'telefone': '(31) 99999-5555',
        'endereco': 'Av. Afonso Pena, 1000',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30140-000',
        'data_nascimento': date(1995, 7, 5),
        'observacoes': 'Prefere roupas esportivas',
        'ativo': True
    },
    {
        'nome': 'Juliana Alves',
        'cpf_cnpj': '654.321.789-00',
        'email': 'juliana.alves@email.com',
        'telefone': '(31) 99999-6666',
        'endereco': 'Rua da Bahia, 567',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30150-000',
        'data_nascimento': date(1993, 9, 12),
        'observacoes': 'Interessada em moda casual',
        'ativo': True
    },
    {
        'nome': 'Roberto Lima',
        'cpf_cnpj': '147.258.369-00',
        'email': 'roberto.lima@email.com',
        'telefone': '(31) 99999-7777',
        'endereco': 'Rua dos Carijós, 890',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30160-000',
        'data_nascimento': date(1987, 2, 18),
        'observacoes': 'Cliente corporativo, compra roupas sociais',
        'ativo': True
    },
    {
        'nome': 'Fernanda Rocha',
        'cpf_cnpj': '258.369.147-00',
        'email': 'fernanda.rocha@email.com',
        'telefone': '(31) 99999-8888',
        'endereco': 'Av. do Contorno, 2000',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30170-000',
        'data_nascimento': date(1991, 6, 30),
        'observacoes': 'Gosta de cores vibrantes',
        'ativo': True
    },
    {
        'nome': 'Lucas Martins',
        'cpf_cnpj': '369.147.258-00',
        'email': 'lucas.martins@email.com',
        'telefone': '(31) 99999-9999',
        'endereco': 'Rua da Glória, 345',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30180-000',
        'data_nascimento': date(1994, 4, 22),
        'observacoes': 'Jovem, prefere estilo despojado',
        'ativo': True
    },
    {
        'nome': 'Patrícia Gomes',
        'cpf_cnpj': '159.357.486-00',
        'email': 'patricia.gomes@email.com',
        'telefone': '(31) 99999-0000',
        'endereco': 'Rua Espírito Santo, 678',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cep': '30190-000',
        'data_nascimento': date(1989, 12, 8),
        'observacoes': 'Cliente fiel há 3 anos',
        'ativo': True
    },
]

clientes_criados = 0
clientes_atualizados = 0

for cliente_data in clientes_data:
    cliente, created = Cliente.objects.get_or_create(
        cpf_cnpj=cliente_data['cpf_cnpj'],
        defaults=cliente_data
    )
    
    if created:
        clientes_criados += 1
        print(f"✅ Cliente criado: {cliente_data['nome']}")
    else:
        # Atualizar dados do cliente existente
        for key, value in cliente_data.items():
            setattr(cliente, key, value)
        cliente.save()
        clientes_atualizados += 1
        print(f"🔄 Cliente atualizado: {cliente_data['nome']}")

print(f"\n✅ Resumo:")
print(f"   - Clientes criados: {clientes_criados}")
print(f"   - Clientes atualizados: {clientes_atualizados}")
print(f"   - Total de clientes: {Cliente.objects.count()}")
print(f"\n🎉 Clientes mockups criados com sucesso!")

