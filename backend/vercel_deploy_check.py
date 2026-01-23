"""
Verificar se o deploy foi atualizado na Vercel
"""

import urllib.request
import json
import time

def check_deploy_update():
    """Verificar se o deploy foi atualizado"""
    
    base_url = "https://smartmanager.vercel.app"
    
    print("=== VERIFICANDO ATUALIZAÇÃO DO DEPLOY ===")
    print(f"URL: {base_url}")
    print("Aguardando atualização do deploy...")
    print()
    
    # Verificar várias vezes se a API foi atualizada
    max_attempts = 10
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Tentativa {attempt}/{max_attempts}...")
        
        try:
            # Testar endpoint de API
            with urllib.request.urlopen(f"{base_url}/api/", timeout=10) as response:
                content = response.read().decode('utf-8')
                
                # Verificar se ainda é HTML ou se virou JSON
                if content.strip().startswith('<!doctype html>') or content.strip().startswith('<html'):
                    print(f"❌ Ainda retornando HTML (tentativa {attempt})")
                    if attempt < max_attempts:
                        print("   Aguardando 30 segundos para próxima verificação...")
                        time.sleep(30)
                    continue
                else:
                    try:
                        json.loads(content)
                        print(f"✅ API ATUALIZADA! (tentativa {attempt})")
                        print()
                        print("🎉 DEPLOY ATUALIZADO COM SUCESSO!")
                        print()
                        print("📋 PRÓXIMOS PASSOS:")
                        print("1. Execute 'deploy_vercel.py' no servidor Vercel")
                        print("2. Acesse: https://smartmanager.vercel.app")
                        print("3. Faça login com: admin / mika123")
                        print("4. Teste criação de categoria")
                        return True
                    except:
                        print(f"❌ Resposta não é JSON válido (tentativa {attempt})")
                        if attempt < max_attempts:
                            print("   Aguardando 30 segundos para próxima verificação...")
                            time.sleep(30)
                        continue
                        
        except Exception as e:
            print(f"❌ Erro na tentativa {attempt}: {e}")
            if attempt < max_attempts:
                print("   Aguardando 30 segundos para próxima verificação...")
                time.sleep(30)
    
    print()
    print("❌ DEPLOY NÃO ATUALIZADO APÓS TODAS AS TENTATIVAS")
    print()
    print("🔧 SOLUÇÕES MANUAIS:")
    print("1. Verifique o dashboard da Vercel")
    print("2. Force um novo deploy manual")
    print("3. Limpe o cache do navegador")
    print("4. Contate o suporte da Vercel")
    
    return False

if __name__ == '__main__':
    check_deploy_update()
