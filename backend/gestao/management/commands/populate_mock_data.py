# -*- coding: utf-8 -*-
"""
Management command para popular o sistema com dados mockups completos
Execute: python manage.py populate_mock_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from estoque.models import Categoria, Produto
from financeiro.models import Cliente, Venda, ItemVenda
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o sistema com dados mockups (categorias, produtos, clientes e vendas)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa dados existentes antes de criar novos',
        )

    def handle(self, *args, **options):
        clear = options['clear']
        
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando população de dados mockups...\n'))

        # Obter ou criar usuário admin
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        if not user.check_password('admin123'):
            user.set_password('admin123')
            user.save()

        # Limpar dados se solicitado
        if clear:
            self.stdout.write(self.style.WARNING('🗑️  Limpando dados existentes...'))
            Venda.objects.all().delete()
            ItemVenda.objects.all().delete()
            Cliente.objects.all().delete()
            Produto.objects.all().delete()
            Categoria.objects.all().delete()

        # 1. Criar Categorias
        self.stdout.write(self.style.SUCCESS('\n1️⃣  Criando Categorias...'))
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
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={'descricao': cat_data['descricao']}
            )
            categorias[cat_data['nome']] = categoria
            if created:
                self.stdout.write(f'   ✅ Categoria criada: {cat_data["nome"]}')

        # 2. Criar Produtos
        self.stdout.write(self.style.SUCCESS('\n2️⃣  Criando Produtos...'))
        produtos_data = [
            # Camisetas
            {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'P', 'cor': 'Branco', 'quantidade': 25, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
            {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 30, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
            {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'G', 'cor': 'Branco', 'quantidade': 20, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
            {'nome': 'Camiseta Básica Preta', 'categoria': 'Camisetas', 'modelo': 'Básica', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 22, 'quantidade_minima': 10, 'preco_custo': 15.00, 'preco_venda': 29.90},
            {'nome': 'Camiseta Estampada Azul', 'categoria': 'Camisetas', 'modelo': 'Estampada', 'tamanho': 'M', 'cor': 'Azul', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
            {'nome': 'Camiseta Polo Branca', 'categoria': 'Camisetas', 'modelo': 'Polo', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 10, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
            {'nome': 'Camiseta Polo Preta', 'categoria': 'Camisetas', 'modelo': 'Polo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 3, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},  # Estoque baixo
            
            # Calças
            {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'modelo': 'Skinny', 'tamanho': '38', 'cor': 'Azul', 'quantidade': 15, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
            {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'modelo': 'Skinny', 'tamanho': '40', 'cor': 'Azul', 'quantidade': 18, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
            {'nome': 'Calça Jeans Reta Preta', 'categoria': 'Calças', 'modelo': 'Reta', 'tamanho': '40', 'cor': 'Preto', 'quantidade': 4, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},  # Estoque baixo
            {'nome': 'Calça Social Preta', 'categoria': 'Calças', 'modelo': 'Social', 'tamanho': '40', 'cor': 'Preto', 'quantidade': 10, 'quantidade_minima': 5, 'preco_custo': 60.00, 'preco_venda': 119.90},
            
            # Vestidos
            {'nome': 'Vestido Midi Floral', 'categoria': 'Vestidos', 'modelo': 'Midi', 'tamanho': 'M', 'cor': 'Floral', 'quantidade': 8, 'quantidade_minima': 3, 'preco_custo': 55.00, 'preco_venda': 109.90},
            {'nome': 'Vestido Longo Preto', 'categoria': 'Vestidos', 'modelo': 'Longo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 7, 'quantidade_minima': 3, 'preco_custo': 80.00, 'preco_venda': 159.90},
            {'nome': 'Vestido Curto Rosa', 'categoria': 'Vestidos', 'modelo': 'Curto', 'tamanho': 'M', 'cor': 'Rosa', 'quantidade': 2, 'quantidade_minima': 3, 'preco_custo': 40.00, 'preco_venda': 79.90},  # Estoque baixo
            
            # Shorts
            {'nome': 'Short Jeans', 'categoria': 'Shorts', 'modelo': 'Jeans', 'tamanho': '40', 'cor': 'Azul', 'quantidade': 15, 'quantidade_minima': 5, 'preco_custo': 30.00, 'preco_venda': 59.90},
            {'nome': 'Short Esportivo Preto', 'categoria': 'Shorts', 'modelo': 'Esportivo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 20, 'quantidade_minima': 10, 'preco_custo': 20.00, 'preco_venda': 39.90},
            
            # Blusas
            {'nome': 'Blusa Manga Longa Branca', 'categoria': 'Blusas', 'modelo': 'Manga Longa', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 14, 'quantidade_minima': 5, 'preco_custo': 25.00, 'preco_venda': 49.90},
            {'nome': 'Blusão Moletom Cinza', 'categoria': 'Blusas', 'modelo': 'Moletom', 'tamanho': 'G', 'cor': 'Cinza', 'quantidade': 9, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},
            
            # Acessórios
            {'nome': 'Cinto Couro Preto', 'categoria': 'Acessórios', 'modelo': 'Couro', 'tamanho': 'Único', 'cor': 'Preto', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
            {'nome': 'Bolsa Tote Preta', 'categoria': 'Acessórios', 'modelo': 'Tote', 'tamanho': 'Único', 'cor': 'Preto', 'quantidade': 6, 'quantidade_minima': 3, 'preco_custo': 45.00, 'preco_venda': 89.90},
        ]

        produtos = []
        for prod_data in produtos_data:
            categoria = categorias[prod_data['categoria']]
            produto, created = Produto.objects.get_or_create(
                nome=prod_data['nome'],
                categoria=categoria,
                tamanho=prod_data['tamanho'],
                cor=prod_data['cor'],
                defaults={
                    'modelo': prod_data['modelo'],
                    'quantidade': prod_data['quantidade'],
                    'quantidade_minima': prod_data['quantidade_minima'],
                    'preco_custo': Decimal(str(prod_data['preco_custo'])),
                    'preco_venda': Decimal(str(prod_data['preco_venda'])),
                    'ativo': True
                }
            )
            produtos.append(produto)

        self.stdout.write(f'   ✅ {len(produtos)} produtos criados/atualizados')

        # 3. Criar Clientes
        self.stdout.write(self.style.SUCCESS('\n3️⃣  Criando Clientes...'))
        clientes_data = [
            {'nome': 'João Silva', 'cpf_cnpj': '123.456.789-00', 'email': 'joao.silva@email.com', 'telefone': '(31) 99999-1111'},
            {'nome': 'Maria Santos', 'cpf_cnpj': '987.654.321-00', 'email': 'maria.santos@email.com', 'telefone': '(31) 99999-2222'},
            {'nome': 'Pedro Oliveira', 'cpf_cnpj': '456.789.123-00', 'email': 'pedro.oliveira@email.com', 'telefone': '(31) 99999-3333'},
            {'nome': 'Ana Costa', 'cpf_cnpj': '789.123.456-00', 'email': 'ana.costa@email.com', 'telefone': '(31) 99999-4444'},
            {'nome': 'Carlos Ferreira', 'cpf_cnpj': '321.654.987-00', 'email': 'carlos.ferreira@email.com', 'telefone': '(31) 99999-5555'},
            {'nome': 'Juliana Alves', 'cpf_cnpj': '654.321.789-00', 'email': 'juliana.alves@email.com', 'telefone': '(31) 99999-6666'},
            {'nome': 'Roberto Lima', 'cpf_cnpj': '147.258.369-00', 'email': 'roberto.lima@email.com', 'telefone': '(31) 99999-7777'},
            {'nome': 'Fernanda Rocha', 'cpf_cnpj': '258.369.147-00', 'email': 'fernanda.rocha@email.com', 'telefone': '(31) 99999-8888'},
        ]

        clientes = []
        for cliente_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                cpf_cnpj=cliente_data['cpf_cnpj'],
                defaults={
                    'nome': cliente_data['nome'],
                    'email': cliente_data['email'],
                    'telefone': cliente_data['telefone'],
                    'ativo': True
                }
            )
            clientes.append(cliente)

        self.stdout.write(f'   ✅ {len(clientes)} clientes criados/atualizados')

        # 4. Criar Vendas (últimos 30 dias)
        self.stdout.write(self.style.SUCCESS('\n4️⃣  Criando Vendas...'))
        
        hoje = timezone.now().date()
        vendas_criadas = 0
        
        # Criar vendas dos últimos 30 dias
        for dia in range(30):
            data_venda = hoje - timedelta(days=dia)
            
            # Criar 1-3 vendas por dia (aleatório)
            num_vendas_dia = random.randint(1, 3)
            
            for _ in range(num_vendas_dia):
                cliente = random.choice(clientes)
                produtos_venda = random.sample(produtos, k=random.randint(1, 4))
                
                # Criar venda
                venda = Venda.objects.create(
                    cliente=cliente,
                    cliente_nome=cliente.nome,
                    status='CONCLUIDA',
                    desconto=Decimal('0.00'),
                    usuario=user,
                    criado_em=timezone.make_aware(
                        timezone.datetime.combine(data_venda, timezone.datetime.min.time())
                    ) + timedelta(hours=random.randint(9, 18))
                )
                
                # Adicionar itens
                total_venda = Decimal('0.00')
                for produto in produtos_venda:
                    quantidade = random.randint(1, 3)
                    preco_unitario = produto.preco_venda
                    
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario
                    )
                    
                    # Atualizar estoque
                    produto.quantidade -= quantidade
                    produto.save()
                    
                    total_venda += preco_unitario * quantidade
                
                # Aplicar desconto ocasional (10% das vendas)
                if random.random() < 0.1:
                    desconto = total_venda * Decimal('0.1')
                    venda.desconto = desconto
                    total_venda -= desconto
                
                venda.total = total_venda
                venda.save()
                vendas_criadas += 1

        self.stdout.write(f'   ✅ {vendas_criadas} vendas criadas')

        # Resumo final
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✅ RESUMO FINAL'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'📦 Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'👕 Produtos: {Produto.objects.count()}')
        self.stdout.write(f'👥 Clientes: {Cliente.objects.count()}')
        self.stdout.write(f'💰 Vendas: {Venda.objects.count()}')
        
        # Estatísticas
        produtos_estoque_baixo = sum(1 for p in Produto.objects.all() if p.estoque_baixo)
        total_vendas = Venda.objects.filter(status='CONCLUIDA').aggregate(
            total=models.Sum('total')
        )['total'] or Decimal('0.00')
        
        self.stdout.write(f'⚠️  Produtos com estoque baixo: {produtos_estoque_baixo}')
        self.stdout.write(f'💵 Total de vendas: R$ {total_vendas:.2f}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Sistema populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS('💡 Acesse o dashboard para ver os dados!'))

