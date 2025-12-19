# -*- coding: utf-8 -*-
"""
Script para criar dados mockups (categorias e produtos de exemplo)
Execute: python manage.py shell -c "exec(open('create_mock_data.py', encoding='utf-8').read())"
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
from django.contrib.auth.models import User

# Criar superusuário se não existir
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superusuário 'admin' criado (senha: admin123)")

# Limpar dados existentes (opcional - descomente se quiser limpar)
# Categoria.objects.all().delete()
# Produto.objects.all().delete()

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
    categoria, created = Categoria.objects.get_or_create(
        nome=cat_data['nome'],
        defaults={'descricao': cat_data['descricao']}
    )
    categorias[cat_data['nome']] = categoria
    if created:
        print(f"✅ Categoria criada: {cat_data['nome']}")

# Produtos de exemplo
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
    {'nome': 'Camiseta Polo Preta', 'categoria': 'Camisetas', 'modelo': 'Polo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 3, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},  # Estoque baixo
    
    # Calças
    {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'modelo': 'Skinny', 'tamanho': '38', 'cor': 'Azul', 'quantidade': 15, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
    {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'modelo': 'Skinny', 'tamanho': '40', 'cor': 'Azul', 'quantidade': 18, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
    {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'modelo': 'Skinny', 'tamanho': '42', 'cor': 'Azul', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
    {'nome': 'Calça Jeans Reta Preta', 'categoria': 'Calças', 'modelo': 'Reta', 'tamanho': '38', 'cor': 'Preto', 'quantidade': 2, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},  # Estoque baixo
    {'nome': 'Calça Jeans Reta Preta', 'categoria': 'Calças', 'modelo': 'Reta', 'tamanho': '40', 'cor': 'Preto', 'quantidade': 4, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},  # Estoque baixo
    {'nome': 'Calça Social Preta', 'categoria': 'Calças', 'modelo': 'Social', 'tamanho': '38', 'cor': 'Preto', 'quantidade': 8, 'quantidade_minima': 5, 'preco_custo': 60.00, 'preco_venda': 119.90},
    {'nome': 'Calça Social Preta', 'categoria': 'Calças', 'modelo': 'Social', 'tamanho': '40', 'cor': 'Preto', 'quantidade': 10, 'quantidade_minima': 5, 'preco_custo': 60.00, 'preco_venda': 119.90},
    {'nome': 'Calça Legging Preta', 'categoria': 'Calças', 'modelo': 'Legging', 'tamanho': 'P', 'cor': 'Preto', 'quantidade': 20, 'quantidade_minima': 10, 'preco_custo': 25.00, 'preco_venda': 49.90},
    {'nome': 'Calça Legging Preta', 'categoria': 'Calças', 'modelo': 'Legging', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 25, 'quantidade_minima': 10, 'preco_custo': 25.00, 'preco_venda': 49.90},
    
    # Vestidos
    {'nome': 'Vestido Midi Floral', 'categoria': 'Vestidos', 'modelo': 'Midi', 'tamanho': 'P', 'cor': 'Floral', 'quantidade': 5, 'quantidade_minima': 3, 'preco_custo': 55.00, 'preco_venda': 109.90},
    {'nome': 'Vestido Midi Floral', 'categoria': 'Vestidos', 'modelo': 'Midi', 'tamanho': 'M', 'cor': 'Floral', 'quantidade': 8, 'quantidade_minima': 3, 'preco_custo': 55.00, 'preco_venda': 109.90},
    {'nome': 'Vestido Midi Floral', 'categoria': 'Vestidos', 'modelo': 'Midi', 'tamanho': 'G', 'cor': 'Floral', 'quantidade': 6, 'quantidade_minima': 3, 'preco_custo': 55.00, 'preco_venda': 109.90},
    {'nome': 'Vestido Longo Preto', 'categoria': 'Vestidos', 'modelo': 'Longo', 'tamanho': 'P', 'cor': 'Preto', 'quantidade': 4, 'quantidade_minima': 3, 'preco_custo': 80.00, 'preco_venda': 159.90},
    {'nome': 'Vestido Longo Preto', 'categoria': 'Vestidos', 'modelo': 'Longo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 7, 'quantidade_minima': 3, 'preco_custo': 80.00, 'preco_venda': 159.90},
    {'nome': 'Vestido Curto Rosa', 'categoria': 'Vestidos', 'modelo': 'Curto', 'tamanho': 'P', 'cor': 'Rosa', 'quantidade': 1, 'quantidade_minima': 3, 'preco_custo': 40.00, 'preco_venda': 79.90},  # Estoque baixo
    {'nome': 'Vestido Curto Rosa', 'categoria': 'Vestidos', 'modelo': 'Curto', 'tamanho': 'M', 'cor': 'Rosa', 'quantidade': 2, 'quantidade_minima': 3, 'preco_custo': 40.00, 'preco_venda': 79.90},  # Estoque baixo
    {'nome': 'Vestido Casual Azul', 'categoria': 'Vestidos', 'modelo': 'Casual', 'tamanho': 'M', 'cor': 'Azul', 'quantidade': 9, 'quantidade_minima': 5, 'preco_custo': 45.00, 'preco_venda': 89.90},
    
    # Shorts
    {'nome': 'Short Jeans', 'categoria': 'Shorts', 'modelo': 'Jeans', 'tamanho': '38', 'cor': 'Azul', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 30.00, 'preco_venda': 59.90},
    {'nome': 'Short Jeans', 'categoria': 'Shorts', 'modelo': 'Jeans', 'tamanho': '40', 'cor': 'Azul', 'quantidade': 15, 'quantidade_minima': 5, 'preco_custo': 30.00, 'preco_venda': 59.90},
    {'nome': 'Short Esportivo Preto', 'categoria': 'Shorts', 'modelo': 'Esportivo', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 20, 'quantidade_minima': 10, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Short Esportivo Preto', 'categoria': 'Shorts', 'modelo': 'Esportivo', 'tamanho': 'G', 'cor': 'Preto', 'quantidade': 18, 'quantidade_minima': 10, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Bermuda Cargo Bege', 'categoria': 'Shorts', 'modelo': 'Cargo', 'tamanho': '40', 'cor': 'Bege', 'quantidade': 6, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
    
    # Blusas
    {'nome': 'Blusa Manga Longa Branca', 'categoria': 'Blusas', 'modelo': 'Manga Longa', 'tamanho': 'P', 'cor': 'Branco', 'quantidade': 10, 'quantidade_minima': 5, 'preco_custo': 25.00, 'preco_venda': 49.90},
    {'nome': 'Blusa Manga Longa Branca', 'categoria': 'Blusas', 'modelo': 'Manga Longa', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 14, 'quantidade_minima': 5, 'preco_custo': 25.00, 'preco_venda': 49.90},
    {'nome': 'Blusa Manga Curta Rosa', 'categoria': 'Blusas', 'modelo': 'Manga Curta', 'tamanho': 'M', 'cor': 'Rosa', 'quantidade': 8, 'quantidade_minima': 5, 'preco_custo': 22.00, 'preco_venda': 44.90},
    {'nome': 'Blusa Manga Curta Rosa', 'categoria': 'Blusas', 'modelo': 'Manga Curta', 'tamanho': 'G', 'cor': 'Rosa', 'quantidade': 6, 'quantidade_minima': 5, 'preco_custo': 22.00, 'preco_venda': 44.90},
    {'nome': 'Blusão Moletom Cinza', 'categoria': 'Blusas', 'modelo': 'Moletom', 'tamanho': 'M', 'cor': 'Cinza', 'quantidade': 11, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},
    {'nome': 'Blusão Moletom Cinza', 'categoria': 'Blusas', 'modelo': 'Moletom', 'tamanho': 'G', 'cor': 'Cinza', 'quantidade': 9, 'quantidade_minima': 5, 'preco_custo': 50.00, 'preco_venda': 99.90},
    
    # Saias
    {'nome': 'Saia Midi Preta', 'categoria': 'Saias', 'modelo': 'Midi', 'tamanho': 'P', 'cor': 'Preto', 'quantidade': 7, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
    {'nome': 'Saia Midi Preta', 'categoria': 'Saias', 'modelo': 'Midi', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 9, 'quantidade_minima': 5, 'preco_custo': 35.00, 'preco_venda': 69.90},
    {'nome': 'Saia Curta Jeans', 'categoria': 'Saias', 'modelo': 'Curta', 'tamanho': 'P', 'cor': 'Azul', 'quantidade': 5, 'quantidade_minima': 3, 'preco_custo': 28.00, 'preco_venda': 55.90},
    {'nome': 'Saia Curta Jeans', 'categoria': 'Saias', 'modelo': 'Curta', 'tamanho': 'M', 'cor': 'Azul', 'quantidade': 8, 'quantidade_minima': 3, 'preco_custo': 28.00, 'preco_venda': 55.90},
    {'nome': 'Saia Longa Estampada', 'categoria': 'Saias', 'modelo': 'Longa', 'tamanho': 'M', 'cor': 'Estampada', 'quantidade': 4, 'quantidade_minima': 3, 'preco_custo': 40.00, 'preco_venda': 79.90},
    
    # Acessórios
    {'nome': 'Cinto Couro Marrom', 'categoria': 'Acessórios', 'modelo': 'Couro', 'tamanho': 'Único', 'cor': 'Marrom', 'quantidade': 15, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Cinto Couro Preto', 'categoria': 'Acessórios', 'modelo': 'Couro', 'tamanho': 'Único', 'cor': 'Preto', 'quantidade': 12, 'quantidade_minima': 5, 'preco_custo': 20.00, 'preco_venda': 39.90},
    {'nome': 'Bolsa Tote Bege', 'categoria': 'Acessórios', 'modelo': 'Tote', 'tamanho': 'Único', 'cor': 'Bege', 'quantidade': 8, 'quantidade_minima': 3, 'preco_custo': 45.00, 'preco_venda': 89.90},
    {'nome': 'Bolsa Tote Preta', 'categoria': 'Acessórios', 'modelo': 'Tote', 'tamanho': 'Único', 'cor': 'Preto', 'quantidade': 6, 'quantidade_minima': 3, 'preco_custo': 45.00, 'preco_venda': 89.90},
]

produtos_criados = 0
produtos_atualizados = 0

for prod_data in produtos_data:
    categoria = categorias[prod_data['categoria']]
    
    # Verificar se produto já existe
    produto_existente = Produto.objects.filter(
        nome=prod_data['nome'],
        categoria=categoria,
        tamanho=prod_data['tamanho'],
        cor=prod_data['cor']
    ).first()
    
    if produto_existente:
        # Atualizar produto existente
        produto_existente.quantidade = prod_data['quantidade']
        produto_existente.quantidade_minima = prod_data['quantidade_minima']
        produto_existente.preco_custo = prod_data['preco_custo']
        produto_existente.preco_venda = prod_data['preco_venda']
        produto_existente.modelo = prod_data['modelo']
        produto_existente.ativo = True
        produto_existente.save()
        produtos_atualizados += 1
    else:
        # Criar novo produto
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

print(f"\n✅ Resumo:")
print(f"   - Categorias: {len(categorias)}")
print(f"   - Produtos criados: {produtos_criados}")
print(f"   - Produtos atualizados: {produtos_atualizados}")
print(f"   - Total de produtos: {Produto.objects.count()}")
print(f"\n🎉 Dados mockups criados com sucesso!")

