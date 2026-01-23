"""
Script simplificado para deploy via GET
"""

import urllib.request
import json

def deploy_users_get():
    """Criar usuários via GET (sem POST)"""
    
    base_url = "https://smartmanager.vercel.app"
    
    print("=== TENTANDO DEPLOY VIA GET ===")
    print(f"URL: {base_url}")
    print()
    
    # Tentar diferentes abordagens
    
    # 1. Verificar se endpoints novos existem
    endpoints_to_test = [
        f"{base_url}/deploy/create-users/",
        f"{base_url}/api/deploy/create-users/",
        f"{base_url}/deploy/status/",
        f"{base_url}/api/deploy/status/",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            print(f"Testando: {endpoint}")
            with urllib.request.urlopen(endpoint, timeout=10) as response:
                status = response.getcode()
                content = response.read().decode('utf-8')
                
                print(f"   Status: {status}")
                
                if status == 200:
                    try:
                        data = json.loads(content)
                        print(f"   ✅ Resposta JSON: {str(data)[:100]}...")
                    except:
                        print(f"   ✅ Resposta: {content[:100]}...")
                else:
                    print(f"   ❌ Resposta: {content[:100]}...")
                print()
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            print()
    
    # 2. Tentar criar usuário via admin (se existir)
    admin_url = f"{base_url}/admin/"
    
    print("=== VERIFICANDO ADMIN ===")
    print(f"URL Admin: {admin_url}")
    
    try:
        with urllib.request.urlopen(admin_url, timeout=10) as response:
            if response.getcode() == 200:
                content = response.read().decode('utf-8')
                if 'login' in content.lower():
                    print("✅ Admin Django está acessível!")
                    print("   Tente acessar diretamente:")
                    print("   1. Acesse a URL acima")
                    print("   2. Faça login com admin/mika123")
                    print("   3. Crie os usuários manualmente")
                    return True
                else:
                    print("❌ Admin não encontrado ou bloqueado")
            else:
                print(f"❌ Admin indisponível: {response.getcode()}")
                
    except Exception as e:
        print(f"❌ Erro ao acessar admin: {e}")
    
    # 3. Instruções finais
    print()
    print("=== INSTRUÇÕES FINAIS ===")
    print("Se nada funcionar:")
    print("1. Verifique se o deploy foi atualizado:")
    print(f"   - Acesse: {base_url}")
    print("   - Deve retornar JSON em /api/")
    print("   - Se retornar HTML, deploy não atualizado")
    print()
    print("2. Tente o admin Django:")
    print(f"   - URL: {admin_url}")
    print("   - User: admin")
    print("   - Password: mika123")
    print()
    print("3. Se tiver acesso ao banco:")
    print("   - Conecte diretamente ao banco")
    print("   - Execute: INSERT INTO auth_user...")
    print()
    print("4. Contate o suporte Vercel")

if __name__ == '__main__':
    deploy_users_get()
