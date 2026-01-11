"""
Testar todos os endpoints da API do deploy Vercel
"""

import urllib.request
import urllib.parse
import json

def test_endpoint(url, method='GET', data=None, description=''):
    """Testar um endpoint específico"""
    try:
        if method == 'POST' and data:
            data_bytes = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={
                    'Content-Type': 'application/json',
                    'Content-Length': len(data_bytes)
                }
            )
        else:
            req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_data = response.read().decode('utf-8')
            
            print(f"{'✅' if status_code == 200 else '❌'} {method} {url}")
            print(f"   Status: {status_code}")
            
            if status_code == 200:
                try:
                    result = json.loads(response_data)
                    if description:
                        print(f"   {description}: {result}")
                    else:
                        print(f"   Response: {str(result)[:100]}...")
                except:
                    print(f"   Response: {response_data[:100]}...")
            else:
                print(f"   Error: {response_data[:200]}...")
            
            print()
            return status_code == 200
            
    except Exception as e:
        print(f"❌ {method} {url}")
        print(f"   Erro: {e}")
        print()
        return False

def test_vercel_endpoints():
    """Testar todos os endpoints importantes"""
    
    base_url = "https://chama-o-mika.vercel.app"
    
    print("=== TESTANDO ENDPOINTS DA API VERCEL ===")
    print(f"Base URL: {base_url}")
    print()
    
    # Testar endpoints
    endpoints = [
        (f"{base_url}/", 'GET', None, 'API Root'),
        (f"{base_url}/api/auth/csrf-token/", 'GET', None, 'CSRF Token'),
        (f"{base_url}/api/auth/login/", 'POST', {'username': 'admin', 'password': 'mika123'}, 'Login'),
        (f"{base_url}/api/auth/user/", 'GET', None, 'User Info'),
        (f"{base_url}/api/estoque/categorias/", 'GET', None, 'Categorias'),
        (f"{base_url}/api/financeiro/relatorios/fluxo_caixa/", 'GET', None, 'Relatório Fluxo Caixa'),
        (f"{base_url}/api/financeiro/relatorios-avancados/fluxo_caixa_completo/", 'GET', None, 'Relatório Avançado'),
    ]
    
    results = []
    for url, method, data, description in endpoints:
        success = test_endpoint(url, method, data, description)
        results.append((url, method, success))
    
    # Resumo
    print("=== RESUMO DOS TESTES ===")
    working = sum(1 for _, _, success in results if success)
    total = len(results)
    
    print(f"Endpoints funcionando: {working}/{total}")
    
    if working < total:
        print("\n⚠️ ALGUNS ENDPOINTS NÃO ESTÃO FUNCIONANDO")
        print("Possíveis causas:")
        print("1. Deploy não atualizado com as últimas mudanças")
        print("2. Configuração CORS no Vercel")
        print("3. Middleware CSRF bloqueando requisições")
        print("4. Variáveis de ambiente incorretas")
        
        print("\n🔧 SOLUÇÕES:")
        print("1. Execute 'deploy_vercel.py' no servidor")
        print("2. Verifique logs no Vercel Dashboard")
        print("3. Confirme se as migrações foram aplicadas")
        print("4. Teste com curl diretamente no servidor")
    else:
        print("\n✅ TODOS OS ENDPOINTS ESTÃO FUNCIONANDO!")
    
    return working == total

if __name__ == '__main__':
    test_vercel_endpoints()
