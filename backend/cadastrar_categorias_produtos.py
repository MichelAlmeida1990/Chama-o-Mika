import os
import django
from decimal import Decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from estoque.models import Categoria, Produto
from django.contrib.auth.models import User

print("=== CADASTRANDO CATEGORIAS E PRODUTOS ===\n")

# Obter usuário para associar aos produtos
try:
    user = User.objects.get(username='mika')
except User.DoesNotExist:
    print("Usuário 'mika' não encontrado. Usando primeiro usuário disponível.")
    user = User.objects.first()

# 1. Cadastrar Categorias
categorias_data = [
    {
        'nome': 'Camisetas',
        'descricao': 'Camisetas de algodão, poliéster e outros materiais'
    },
    {
        'nome': 'Calças',
        'descricao': 'Calças jeans, sociais, esportivas e outros'
    },
    {
        'nome': 'Vestidos',
        'descricao': 'Vestidos curtos, longos, sociais e festivos'
    },
    {
        'nome': 'Blusas',
        'descricao': 'Blusas femininas em diversos estilos e materiais'
    },
    {
        'nome': 'Shorts',
        'descricao': 'Shorts masculinos e femininos'
    },
    {
        'nome': 'Tênis',
        'descricao': 'Tênis esportivos e casuais'
    },
    {
        'nome': 'Sandálias',
        'descricao': 'Sandálias e chinelos diversos'
    },
    {
        'nome': 'Acessórios',
        'descricao': 'Bolsas, cintos, meias e outros acessórios'
    }
]

print("1. Cadastrando CATEGORIAS...")
categorias_criadas = []
for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nome=cat_data['nome'],
        defaults={'descricao': cat_data['descricao']}
    )
    categorias_criadas.append(categoria)
    if created:
        print(f"   ✅ {categoria.nome} - criada")
    else:
        print(f"   ⚠️  {categoria.nome} - já existia")

# 2. Cadastrar Produtos
produtos_data = [
    # Camisetas
    {'categoria': 'Camisetas', 'nome': 'Camiseta Básica Branca', 'modelo': 'Classic', 'tamanho': 'P', 'cor': 'Branco', 'qtd': 20, 'qtd_min': 5, 'custo': 15.00, 'venda': 35.00},
    {'categoria': 'Camisetas', 'nome': 'Camiseta Básica Branca', 'modelo': 'Classic', 'tamanho': 'M', 'cor': 'Branco', 'qtd': 25, 'qtd_min': 5, 'custo': 15.00, 'venda': 35.00},
    {'categoria': 'Camisetas', 'nome': 'Camiseta Básica Branca', 'modelo': 'Classic', 'tamanho': 'G', 'cor': 'Branco', 'qtd': 15, 'qtd_min': 5, 'custo': 15.00, 'venda': 35.00},
    {'categoria': 'Camisetas', 'nome': 'Camiseta Estampa Florida', 'modelo': 'Summer', 'tamanho': 'P', 'cor': 'Azul', 'qtd': 12, 'qtd_min': 3, 'custo': 22.00, 'venda': 49.90},
    {'categoria': 'Camisetas', 'nome': 'Camiseta Estampa Florida', 'modelo': 'Summer', 'tamanho': 'M', 'cor': 'Azul', 'qtd': 18, 'qtd_min': 3, 'custo': 22.00, 'venda': 49.90},
    {'categoria': 'Camisetas', 'nome': 'Camiseta Estampa Florida', 'modelo': 'Summer', 'tamanho': 'G', 'cor': 'Azul', 'qtd': 10, 'qtd_min': 3, 'custo': 22.00, 'venda': 49.90},
    
    # Calças
    {'categoria': 'Calças', 'nome': 'Calça Jeans Feminina', 'modelo': 'Skinny', 'tamanho': '36', 'cor': 'Azul Escuro', 'qtd': 8, 'qtd_min': 2, 'custo': 45.00, 'venda': 89.90},
    {'categoria': 'Calças', 'nome': 'Calça Jeans Feminina', 'modelo': 'Skinny', 'tamanho': '38', 'cor': 'Azul Escuro', 'qtd': 12, 'qtd_min': 2, 'custo': 45.00, 'venda': 89.90},
    {'categoria': 'Calças', 'nome': 'Calça Jeans Masculina', 'modelo': 'Straight', 'tamanho': '40', 'cor': 'Azul Médio', 'qtd': 10, 'qtd_min': 2, 'custo': 55.00, 'venda': 109.90},
    {'categoria': 'Calças', 'nome': 'Calça Jeans Masculina', 'modelo': 'Straight', 'tamanho': '42', 'cor': 'Azul Médio', 'qtd': 8, 'qtd_min': 2, 'custo': 55.00, 'venda': 109.90},
    {'categoria': 'Calças', 'nome': 'Calça Social Masculina', 'modelo': 'Executive', 'tamanho': '40', 'cor': 'Preto', 'qtd': 6, 'qtd_min': 2, 'custo': 75.00, 'venda': 149.90},
    {'categoria': 'Calças', 'nome': 'Calça Social Masculina', 'modelo': 'Executive', 'tamanho': '42', 'cor': 'Preto', 'qtd': 6, 'qtd_min': 2, 'custo': 75.00, 'venda': 149.90},
    
    # Vestidos
    {'categoria': 'Vestidos', 'nome': 'Vestido Longo Festivo', 'modelo': 'Elegant', 'tamanho': 'P', 'cor': 'Vermelho', 'qtd': 5, 'qtd_min': 1, 'custo': 120.00, 'venda': 249.90},
    {'categoria': 'Vestidos', 'nome': 'Vestido Longo Festivo', 'modelo': 'Elegant', 'tamanho': 'M', 'cor': 'Vermelho', 'qtd': 7, 'qtd_min': 1, 'custo': 120.00, 'venda': 249.90},
    {'categoria': 'Vestidos', 'nome': 'Vestido Curto Casual', 'modelo': 'Summer', 'tamanho': 'P', 'cor': 'Floral', 'qtd': 10, 'qtd_min': 2, 'custo': 35.00, 'venda': 79.90},
    {'categoria': 'Vestidos', 'nome': 'Vestido Curto Casual', 'modelo': 'Summer', 'tamanho': 'M', 'cor': 'Floral', 'qtd': 12, 'qtd_min': 2, 'custo': 35.00, 'venda': 79.90},
    
    # Blusas
    {'categoria': 'Blusas', 'nome': 'Blusa Feminina Renda', 'modelo': 'Delicate', 'tamanho': 'P', 'cor': 'Branco', 'qtd': 8, 'qtd_min': 2, 'custo': 38.00, 'venda': 89.90},
    {'categoria': 'Blusas', 'nome': 'Blusa Feminina Renda', 'modelo': 'Delicate', 'tamanho': 'M', 'cor': 'Branco', 'qtd': 10, 'qtd_min': 2, 'custo': 38.00, 'venda': 89.90},
    {'categoria': 'Blusas', 'nome': 'Blusa Ciganinha', 'modelo': 'Boho', 'tamanho': 'P', 'cor': 'Laranja', 'qtd': 6, 'qtd_min': 1, 'custo': 42.00, 'venda': 99.90},
    {'categoria': 'Blusas', 'nome': 'Blusa Ciganinha', 'modelo': 'Boho', 'tamanho': 'M', 'cor': 'Laranja', 'qtd': 8, 'qtd_min': 1, 'custo': 42.00, 'venda': 99.90},
    
    # Shorts
    {'categoria': 'Shorts', 'nome': 'Short Jeans Feminino', 'modelo': 'Casual', 'tamanho': '36', 'cor': 'Azul Claro', 'qtd': 15, 'qtd_min': 3, 'custo': 28.00, 'venda': 59.90},
    {'categoria': 'Shorts', 'nome': 'Short Jeans Feminino', 'modelo': 'Casual', 'tamanho': '38', 'cor': 'Azul Claro', 'qtd': 18, 'qtd_min': 3, 'custo': 28.00, 'venda': 59.90},
    {'categoria': 'Shorts', 'nome': 'Short Bermuda Masculina', 'modelo': 'Beach', 'tamanho': 'M', 'cor': 'Cáqui', 'qtd': 12, 'qtd_min': 2, 'custo': 32.00, 'venda': 69.90},
    {'categoria': 'Shorts', 'nome': 'Short Bermuda Masculina', 'modelo': 'Beach', 'tamanho': 'G', 'cor': 'Cáqui', 'qtd': 10, 'qtd_min': 2, 'custo': 32.00, 'venda': 69.90},
    
    # Tênis
    {'categoria': 'Tênis', 'nome': 'Tênis Esportivo', 'modelo': 'Runner', 'tamanho': '38', 'cor': 'Preto', 'qtd': 8, 'qtd_min': 2, 'custo': 85.00, 'venda': 189.90},
    {'categoria': 'Tênis', 'nome': 'Tênis Esportivo', 'modelo': 'Runner', 'tamanho': '39', 'cor': 'Preto', 'qtd': 10, 'qtd_min': 2, 'custo': 85.00, 'venda': 189.90},
    {'categoria': 'Tênis', 'nome': 'Tênis Esportivo', 'modelo': 'Runner', 'tamanho': '40', 'cor': 'Preto', 'qtd': 12, 'qtd_min': 2, 'custo': 85.00, 'venda': 189.90},
    {'categoria': 'Tênis', 'nome': 'Tênis Casual', 'modelo': 'Urban', 'tamanho': '41', 'cor': 'Branco', 'qtd': 6, 'qtd_min': 1, 'custo': 95.00, 'venda': 219.90},
    {'categoria': 'Tênis', 'nome': 'Tênis Casual', 'modelo': 'Urban', 'tamanho': '42', 'cor': 'Branco', 'qtd': 8, 'qtd_min': 1, 'custo': 95.00, 'venda': 219.90},
    
    # Sandálias
    {'categoria': 'Sandálias', 'nome': 'Sandália Feminina', 'modelo': 'Beach', 'tamanho': '36', 'cor': 'Marrom', 'qtd': 20, 'qtd_min': 4, 'custo': 25.00, 'venda': 54.90},
    {'categoria': 'Sandálias', 'nome': 'Sandália Feminina', 'modelo': 'Beach', 'tamanho': '37', 'cor': 'Marrom', 'qtd': 22, 'qtd_min': 4, 'custo': 25.00, 'venda': 54.90},
    {'categoria': 'Sandálias', 'nome': 'Chinelo Masculino', 'modelo': 'Basic', 'tamanho': '40', 'cor': 'Azul', 'qtd': 25, 'qtd_min': 5, 'custo': 18.00, 'venda': 39.90},
    {'categoria': 'Sandálias', 'nome': 'Chinelo Masculino', 'modelo': 'Basic', 'tamanho': '42', 'cor': 'Azul', 'qtd': 20, 'qtd_min': 5, 'custo': 18.00, 'venda': 39.90},
    
    # Acessórios
    {'categoria': 'Acessórios', 'nome': 'Bolsa Feminina', 'modelo': 'Fashion', 'tamanho': 'Único', 'cor': 'Preto', 'qtd': 10, 'qtd_min': 2, 'custo': 65.00, 'venda': 149.90},
    {'categoria': 'Acessórios', 'nome': 'Bolsa Feminina', 'modelo': 'Fashion', 'tamanho': 'Único', 'cor': 'Marrom', 'qtd': 8, 'qtd_min': 2, 'custo': 65.00, 'venda': 149.90},
    {'categoria': 'Acessórios', 'nome': 'Cinto Masculino', 'modelo': 'Classic', 'tamanho': 'Único', 'cor': 'Preto', 'qtd': 15, 'qtd_min': 3, 'custo': 22.00, 'venda': 49.90},
    {'categoria': 'Acessórios', 'nome': 'Cinto Masculino', 'modelo': 'Classic', 'tamanho': 'Único', 'cor': 'Marrom', 'qtd': 12, 'qtd_min': 3, 'custo': 22.00, 'venda': 49.90},
]

print("\n2. Cadastrando PRODUTOS...")
produtos_criados = 0
produtos_atualizados = 0

for prod_data in produtos_data:
    # Encontrar a categoria
    categoria = next((cat for cat in categorias_criadas if cat.nome == prod_data['categoria']), None)
    if not categoria:
        print(f"   ❌ Categoria '{prod_data['categoria']}' não encontrada")
        continue
    
    # Verificar se o produto já existe
    produto, created = Produto.objects.get_or_create(
        nome=prod_data['nome'],
        tamanho=prod_data['tamanho'],
        cor=prod_data['cor'],
        modelo=prod_data['modelo'],
        defaults={
            'categoria': categoria,
            'quantidade': prod_data['qtd'],
            'quantidade_minima': prod_data['qtd_min'],
            'preco_custo': Decimal(str(prod_data['custo'])),
            'preco_venda': Decimal(str(prod_data['venda'])),
            'descricao': f'{prod_data["nome"]} - Modelo {prod_data["modelo"]}',
            'ativo': True
        }
    )
    
    if created:
        produtos_criados += 1
        print(f"   ✅ {produto.nome} - {produto.tamanho} - {produto.cor} - R$ {produto.preco_venda}")
    else:
        # Atualizar produto existente
        produto.quantidade = prod_data['qtd']
        produto.quantidade_minima = prod_data['qtd_min']
        produto.preco_custo = Decimal(str(prod_data['custo']))
        produto.preco_venda = Decimal(str(prod_data['venda']))
        produto.save()
        produtos_atualizados += 1
        print(f"   🔄 {produto.nome} - {produto.tamanho} - {produto.cor} - atualizado")

# Resumo
print(f"\n=== RESUMO DO CADASTRO ===")
print(f"Categorias criadas: {len([c for c in categorias_criadas if Categoria.objects.filter(nome=c.nome).exists()])}")
print(f"Produtos criados: {produtos_criados}")
print(f"Produtos atualizados: {produtos_atualizados}")
print(f"Total de produtos no sistema: {Produto.objects.count()}")
print(f"Valor total em estoque: R$ {sum(p.quantidade * p.preco_custo for p in Produto.objects.all()):.2f}")
print(f"Valor total de venda: R$ {sum(p.quantidade * p.preco_venda for p in Produto.objects.all()):.2f}")

print("\n=== DADOS CADASTRADOS COM SUCESSO ===")
print("Agora você pode acessar o sistema e simular vendas!")
