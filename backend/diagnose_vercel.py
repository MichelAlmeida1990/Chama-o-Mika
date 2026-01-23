"""
Diagnóstico completo do deploy Vercel
"""

import urllib.request
import json

def diagnose_vercel():
    """Diagnosticar problemas no deploy Vercel"""
    
    base_url = "https://smartmanager.vercel.app"
    
    print("=== DIAGNÓSTICO COMPLETO DO DEPLOY VERCEL ===")
    print(f"URL: {base_url}")
    print()
    
    # 1. Verificar se é HTML ou JSON
    print("1. VERIFICANDO TIPO DE RESPOSTA:")
    
    try:
        with urllib.request.urlopen(f"{base_url}/api/", timeout=10) as response:
            content = response.read().decode('utf-8')
            
            if content.strip().startswith('<!doctype html>') or content.strip().startswith('<html'):
                print("❌ PROBLEMA: API está retornando HTML")
                print("   Isso indica que o Django não está configurado para servir JSON")
                print("   Possível causa: Deploy desatualizado ou configuração incorreta")
            else:
                try:
                    json.loads(content)
                    print("✅ API está retornando JSON corretamente")
                except:
                    print("❌ PROBLEMA: Resposta não é HTML nem JSON válido")
            
            print(f"   Primeiros 200 chars: {content[:200]}")
            print()
    
    except Exception as e:
        print(f"❌ Erro ao acessar API: {e}")
        print()
    
    # 2. Verificar headers da resposta
    print("2. VERIFICANDO HEADERS DA RESPOSTA:")
    
    try:
        req = urllib.request.Request(f"{base_url}/api/auth/login/", method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.headers)
            print(f"   Content-Type: {headers.get('Content-Type', 'Não encontrado')}")
            print(f"   Server: {headers.get('Server', 'Não encontrado')}")
            print(f"   Status: {response.getcode()}")
            
            if 'text/html' in headers.get('Content-Type', ''):
                print("❌ PROBLEMA: Server está respondendo com HTML")
            elif 'application/json' in headers.get('Content-Type', ''):
                print("✅ Server está respondendo com JSON")
            else:
                print("⚠️ Content-Type inesperado")
            print()
    
    except Exception as e:
        print(f"❌ Erro ao verificar headers: {e}")
        print()
    
    # 3. Tentar diferentes endpoints
    print("3. TESTANDO ENDPOINTS ESPECÍFICOS:")
    
    endpoints_to_test = [
        f"{base_url}/api/",
        f"{base_url}/api/auth/",
        f"{base_url}/api/estoque/",
        f"{base_url}/api/financeiro/",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            with urllib.request.urlopen(endpoint, timeout=5) as response:
                content = response.read().decode('utf-8')
                is_html = content.strip().startswith('<!doctype') or content.strip().startswith('<html')
                
                status = "✅ OK" if response.getcode() == 200 else "❌ ERRO"
                content_type = "HTML" if is_html else "JSON/Dados"
                
                print(f"   {endpoint}: {status} (Status {response.getcode()}, {content_type})")
                
        except Exception as e:
            print(f"   {endpoint}: ❌ ERRO - {e}")
    
    print()
    
    # 4. Soluções recomendadas
    print("4. SOLUÇÕES RECOMENDADAS:")
    print()
    print("🔧 AÇÃO IMEDIATA:")
    print("1. VERIFICAR SE O DEPLOY ESTÁ ATUALIZADO:")
    print("   - Acesse: https://vercel.com/dashboard")
    print("   - Verifique o último deploy")
    print("   - Confirme se as mudanças foram aplicadas")
    print()
    print("2. EXECUTAR MIGRAÇÕES NO SERVIDOR:")
    print("   - Conecte ao servidor Vercel")
    print("   - Execute: python manage.py migrate")
    print("   - Execute: python deploy_vercel.py")
    print()
    print("3. VERIFICAR VARIÁVEIS DE AMBIENTE:")
    print("   - DEBUG=False em produção")
    print("   - ALLOWED_HOSTS configurado")
    print("   - CORS configurado")
    print()
    print("📋 SE O PROBLEMA PERSISTIR:")
    print("1. O deploy pode estar servindo o frontend em vez da API")
    print("2. Pode haver conflito de rotas")
    print("3. O Vercel pode estar cacheando o deploy antigo")
    print()
    print("🚀 PRÓXIMOS PASSOS:")
    print("1. Faça um novo deploy manual")
    print("2. Limpe o cache do Vercel")
    print("3. Teste novamente com os scripts acima")

if __name__ == '__main__':
    diagnose_vercel()
