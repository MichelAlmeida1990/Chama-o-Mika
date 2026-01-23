import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from estoque.models import Categoria, Produto
from financeiro.models import Cliente, Venda, ItemVenda
from django.contrib.auth.models import User
from django.db import models

print("=" * 60)
print("📊 RESUMO COMPLETO DOS DADOS SIMULADOS")
print("=" * 60)

# Categorias
categorias = Categoria.objects.all()
print(f"\n📂 CATEGORIAS CADASTRADAS: {categorias.count()}")
for cat in categorias:
    produtos_cat = cat.produtos.count()
    print(f"   • {cat.nome}: {produtos_cat} produtos")

# Produtos
produtos = Produto.objects.all()
total_produtos = produtos.count()
produtos_ativos = produtos.filter(ativo=True).count()
estoque_total = produtos.aggregate(total=models.Sum('quantidade'))['total'] or 0
valor_estoque = produtos.aggregate(
    total=models.Sum(models.F('quantidade') * models.F('preco_custo'))
)['total'] or Decimal('0')

print(f"\n👕 PRODUTOS:")
print(f"   • Total de produtos: {total_produtos}")
print(f"   • Produtos ativos: {produtos_ativos}")
print(f"   • Unidades em estoque: {estoque_total}")
print(f"   • Valor total em estoque: R$ {valor_estoque:.2f}")

# Produtos com estoque baixo
baixo_estoque = produtos.filter(quantidade__lte=models.F('quantidade_minima'), ativo=True)
if baixo_estoque.exists():
    print(f"   ⚠️  Produtos com estoque baixo: {baixo_estoque.count()}")
    for p in baixo_estoque[:5]:  # Mostrar apenas 5
        print(f"      - {p.nome} ({p.quantidade} unid)")

# Clientes
clientes = Cliente.objects.all()
clientes_ativos = clientes.filter(ativo=True).count()
print(f"\n👥 CLIENTES:")
print(f"   • Total de clientes: {clientes.count()}")
print(f"   • Clientes ativos: {clientes_ativos}")

# Vendas
vendas = Venda.objects.all()
total_vendas = vendas.count()
valor_vendas = vendas.aggregate(total=models.Sum('total'))['total'] or Decimal('0')
ticket_medio = valor_vendas / total_vendas if total_vendas > 0 else Decimal('0')

print(f"\n💰 VENDAS:")
print(f"   • Total de vendas: {total_vendas}")
print(f"   • Faturamento total: R$ {valor_vendas:.2f}")
print(f"   • Ticket médio: R$ {ticket_medio:.2f}")

# Produtos mais vendidos
itens_vendidos = ItemVenda.objects.values('produto__nome').annotate(
    total_quantidade=models.Sum('quantidade'),
    total_valor=models.Sum(models.F('quantidade') * models.F('preco_unitario'))
).order_by('-total_quantidade')[:5]

if itens_vendidos:
    print(f"\n🏆 PRODUTOS MAIS VENDIDOS:")
    for item in itens_vendidos:
        print(f"   • {item['produto__nome']}: {item['total_quantidade']} unid - R$ {item['total_valor']:.2f}")

# Usuários
usuarios = User.objects.all()
print(f"\n👤 USUÁRIOS DO SISTEMA: {usuarios.count()}")
for user in usuarios:
    print(f"   • {user.username} ({user.email or 'sem email'})")

print("\n" + "=" * 60)
print("✅ SISTEMA PRONTO PARA USO!")
print("🌐 Acesse: http://localhost:3000")
print("🔧 Backend: http://127.0.0.1:8000")
print("=" * 60)
