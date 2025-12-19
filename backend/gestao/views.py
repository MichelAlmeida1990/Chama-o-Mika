from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from django.conf import settings
import json
import os


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """View para autenticação de usuário"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Usuário ou senha inválidos'
            }, status=401)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """View para logout de usuário"""
    logout(request)
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def user_view(request):
    """View para obter informações do usuário logado"""
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })
    else:
        return JsonResponse({'error': 'Não autenticado'}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def populate_mock_data_view(request):
    """
    Endpoint temporário para popular dados mockups
    Protegido por variável de ambiente POPULATE_SECRET
    Não requer autenticação (bypass do DRF permissions)
    """
    # Verificar secret (se configurado)
    populate_secret = os.environ.get('POPULATE_SECRET', '')
    if populate_secret:
        # Aceita secret via POST, header ou query string
        provided_secret = (
            request.POST.get('secret') or 
            request.headers.get('X-Populate-Secret', '') or
            request.GET.get('secret', '')
        )
        if provided_secret != populate_secret:
            return JsonResponse({'error': 'Secret inválido'}, status=403)
    
    try:
        # Tentar executar o comando primeiro
        try:
            from io import StringIO
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            call_command('populate_mock_data')
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return JsonResponse({
                'success': True,
                'message': 'Dados mockups criados com sucesso!',
                'output': output
            })
        except Exception as cmd_error:
            # Se o comando não existir, criar dados diretamente
            if 'Unknown command' in str(cmd_error):
                # Importar e executar a lógica diretamente
                from estoque.models import Categoria, Produto
                from financeiro.models import Cliente, Venda, ItemVenda
                from django.contrib.auth import get_user_model
                from django.utils import timezone
                from datetime import timedelta
                from decimal import Decimal
                import random
                
                User = get_user_model()
                output_lines = []
                
                # Obter ou criar usuário admin
                user, _ = User.objects.get_or_create(
                    username='admin',
                    defaults={'email': 'admin@example.com', 'is_superuser': True, 'is_staff': True}
                )
                
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
                        output_lines.append(f"Categoria criada: {cat_data['nome']}")
                
                # Criar alguns produtos
                produtos_data = [
                    {'nome': 'Camiseta Básica Branca', 'categoria': 'Camisetas', 'tamanho': 'M', 'cor': 'Branco', 'quantidade': 30, 'preco_custo': 15.00, 'preco_venda': 29.90},
                    {'nome': 'Camiseta Básica Preta', 'categoria': 'Camisetas', 'tamanho': 'M', 'cor': 'Preto', 'quantidade': 22, 'preco_custo': 15.00, 'preco_venda': 29.90},
                    {'nome': 'Calça Jeans Skinny', 'categoria': 'Calças', 'tamanho': '40', 'cor': 'Azul', 'quantidade': 18, 'preco_custo': 45.00, 'preco_venda': 89.90},
                    {'nome': 'Vestido Midi Floral', 'categoria': 'Vestidos', 'tamanho': 'M', 'cor': 'Floral', 'quantidade': 8, 'preco_custo': 55.00, 'preco_venda': 109.90},
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
                            'quantidade': prod_data['quantidade'],
                            'quantidade_minima': 5,
                            'preco_custo': Decimal(str(prod_data['preco_custo'])),
                            'preco_venda': Decimal(str(prod_data['preco_venda'])),
                            'ativo': True
                        }
                    )
                    produtos.append(produto)
                    if created:
                        output_lines.append(f"Produto criado: {prod_data['nome']}")
                
                # Criar clientes
                clientes_data = [
                    {'nome': 'João Silva', 'cpf_cnpj': '123.456.789-00', 'email': 'joao.silva@email.com'},
                    {'nome': 'Maria Santos', 'cpf_cnpj': '987.654.321-00', 'email': 'maria.santos@email.com'},
                    {'nome': 'Pedro Oliveira', 'cpf_cnpj': '456.789.123-00', 'email': 'pedro.oliveira@email.com'},
                ]
                
                clientes = []
                for cliente_data in clientes_data:
                    cliente, created = Cliente.objects.get_or_create(
                        cpf_cnpj=cliente_data['cpf_cnpj'],
                        defaults={
                            'nome': cliente_data['nome'],
                            'email': cliente_data['email'],
                            'ativo': True
                        }
                    )
                    clientes.append(cliente)
                    if created:
                        output_lines.append(f"Cliente criado: {cliente_data['nome']}")
                
                # Criar algumas vendas
                hoje = timezone.now().date()
                vendas_criadas = 0
                
                for dia in range(7):  # Últimos 7 dias
                    data_venda = hoje - timedelta(days=dia)
                    num_vendas = random.randint(1, 3)
                    
                    for _ in range(num_vendas):
                        cliente = random.choice(clientes)
                        produtos_venda = random.sample(produtos, k=min(random.randint(1, 3), len(produtos)))
                        
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
                        
                        total_venda = Decimal('0.00')
                        for produto in produtos_venda:
                            quantidade = random.randint(1, 2)
                            preco_unitario = produto.preco_venda
                            
                            ItemVenda.objects.create(
                                venda=venda,
                                produto=produto,
                                quantidade=quantidade,
                                preco_unitario=preco_unitario
                            )
                            
                            produto.quantidade -= quantidade
                            produto.save()
                            total_venda += preco_unitario * quantidade
                        
                        venda.total = total_venda
                        venda.save()
                        vendas_criadas += 1
                
                output_lines.append(f"\nResumo:")
                output_lines.append(f"Categorias: {Categoria.objects.count()}")
                output_lines.append(f"Produtos: {Produto.objects.count()}")
                output_lines.append(f"Clientes: {Cliente.objects.count()}")
                output_lines.append(f"Vendas: {Venda.objects.count()}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Dados mockups criados com sucesso!',
                    'output': '\n'.join(output_lines)
                })
            else:
                raise cmd_error
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc() if settings.DEBUG else None
        }, status=500)


