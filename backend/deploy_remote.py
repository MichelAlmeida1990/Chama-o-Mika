"""
Script para criar usuários remotamente via HTTP
"""

import urllib.request
import urllib.parse
import json
import time

def create_users_remotely():
    """Criar usuários no deploy via requisição HTTP"""
    
    base_url = "https://chama-o-mika.vercel.app"
    deploy_url = f"{base_url}/deploy/create-users/"
    
    print("=== CRIANDO USUÁRIOS REMOTAMENTE ===")
    print(f"URL: {deploy_url}")
    print()
    
    # Dados para criar usuários
    deploy_data = {
        'deploy_key': 'chamaomika2026deploy'
    }
    
    try:
        # Preparar requisição
        data_bytes = json.dumps(deploy_data).encode('utf-8')
        
        req = urllib.request.Request(
            deploy_url,
            data=data_bytes,
            headers={
                'Content-Type': 'application/json',
                'Content-Length': len(data_bytes)
            }
        )
        
        # Enviar requisição
        print("Enviando requisição para criar usuários...")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_data = response.read().decode('utf-8')
            
            if status_code == 200:
                result = json.loads(response_data)
                
                if result.get('success'):
                    print("✅ USUÁRIOS CRIADOS COM SUCESSO!")
                    print()
                    print("Usuários criados:")
                    for user in result.get('users_created', []):
                        print(f"   ✅ {user}")
                    
                    print()
                    print("Credenciais para acesso:")
                    credentials = result.get('credentials', {})
                    for username, password in credentials.items():
                        print(f"   {username} / {password}")
                    
                    print()
                    print("🚀 AGUARDE 1 MINUTO E TENTE O LOGIN!")
                    print("📱 Acesse: https://chama-o-mika.vercel.app")
                    print()
                    print("⏰ AGUARDANDO 60 SEGUNDOS PARA VERIFICAR...")
                    time.sleep(60)
                    
                    # Verificar se funcionou
                    verify_url = f"{base_url}/deploy/status/"
                    with urllib.request.urlopen(verify_url, timeout=10) as verify_response:
                        verify_data = json.loads(verify_response.read().decode('utf-8'))
                        
                        if verify_data.get('success') and verify_data.get('user_count', 0) >= 3:
                            print("✅ DEPLOY CONFIGURADO COM SUCESSO!")
                            print("✅ Usuários criados e funcionando!")
                            return True
                        else:
                            print("⚠️ Usuários criados mas verificação falhou")
                            print(f"   Usuários encontrados: {verify_data.get('user_count', 0)}")
                            return False
                else:
                    print(f"❌ Erro na resposta: {result.get('message', 'Erro desconhecido')}")
                    return False
            else:
                print(f"❌ Erro HTTP {status_code}")
                print(f"   Response: {response_data}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def check_current_status():
    """Verificar status atual do deploy"""
    
    base_url = "https://chama-o-mika.vercel.app"
    status_url = f"{base_url}/deploy/status/"
    
    print("=== VERIFICANDO STATUS ATUAL ===")
    print(f"URL: {status_url}")
    
    try:
        with urllib.request.urlopen(status_url, timeout=10) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                
                print(f"✅ API funcionando: {data.get('api_working', False)}")
                print(f"✅ Usuários encontrados: {data.get('user_count', 0)}")
                
                if data.get('users'):
                    print("Usuários atuais:")
                    for user in data.get('users', []):
                        print(f"   - {user.get('username')} (Ativo: {user.get('is_active', False)})")
                
                return data
            else:
                print(f"❌ Erro ao verificar status: {response.getcode()}")
                return None
                
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return None

if __name__ == '__main__':
    print("Escolha uma opção:")
    print("1. Verificar status atual")
    print("2. Criar usuários remotamente")
    
    choice = input("Digite 1 ou 2: ").strip()
    
    if choice == '1':
        check_current_status()
    elif choice == '2':
        create_users_remotely()
    else:
        print("Opção inválida")
