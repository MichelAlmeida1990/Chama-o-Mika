"""
Testar API do deploy Vercel usando urllib (sem requests)
"""

import urllib.request
import urllib.parse
import json

def test_vercel_login():
    """Testar login na API do Vercel"""
    
    print("=== TESTANDO API DO DEPLOY VERCEL ===")
    print("URL: https://smartmanager.vercel.app")
    print()
    
    login_url = "https://smartmanager.vercel.app/api/auth/login/"
    
    test_credentials = [
        ('admin', 'mika123'),
        ('mika', 'mika123'),
        ('rafael@chamaomika.com', 'mika123')
    ]
    
    for username, password in test_credentials:
        try:
            # Preparar dados
            data = json.dumps({
                'username': username,
                'password': password
            }).encode('utf-8')
            
            # Criar requisição
            req = urllib.request.Request(
                login_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Content-Length': len(data)
                }
            )
            
            # Enviar requisição
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                response_data = response.read().decode('utf-8')
                
                if status_code == 200:
                    print(f"✅ {username}/{password}: Login OK")
                    result = json.loads(response_data)
                    print(f"   User: {result.get('user', {}).get('username', 'N/A')}")
                elif status_code == 400:
                    print(f"❌ {username}/{password}: Credenciais inválidas")
                    try:
                        error_data = json.loads(response_data)
                        print(f"   Erro: {error_data}")
                    except:
                        pass
                else:
                    print(f"⚠️ {username}/{password}: Status {status_code}")
                    print(f"   Response: {response_data}")
                    
        except Exception as e:
            print(f"❌ Erro ao testar {username}: {e}")
    
    print(f"\n=== INSTRUÇÕES PARA O DEPLOY ===")
    print("1. Execute 'deploy_vercel.py' no servidor Vercel")
    print("2. Acesse: https://smartmanager.vercel.app")
    print("3. Use as credenciais acima para login")
    print("4. Se ainda falhar, verifique os logs do Vercel")

if __name__ == '__main__':
    test_vercel_login()
