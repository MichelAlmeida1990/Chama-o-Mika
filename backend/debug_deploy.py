"""
Script para debug completo do deploy
"""

import urllib.request
import json
import time

def debug_deploy():
    """Debug completo do deploy"""
    
    print("=== DEBUG COMPLETO DO DEPLOY ===")
    print()
    
    # URLs para testar
    urls_to_test = [
        ("Frontend Principal", "https://smartmanager.vercel.app"),
        ("Frontend Login", "https://smartmanager.vercel.app/login"),
        ("Backend API", "https://smartmanager.vercel.app/api"),
        ("Backend Auth", "https://smartmanager.vercel.app/api/auth/login"),
        ("Backend Status", "https://smartmanager.vercel.app/api/auth/user"),
        ("Backend Categorias", "https://smartmanager.vercel.app/api/estoque/categorias"),
        ("Backend Deploy", "https://smartmanager-backend.onrender.com"),
        ("Backend API Render", "https://smartmanager-backend.onrender.com/api"),
    ]
    
    print("1. TESTANDO TODAS AS URLs:")
    print()
    
    working_urls = []
    broken_urls = []
    
    for name, url in urls_to_test:
        try:
            print(f"Testando: {name}")
            print(f"URL: {url}")
            
            with urllib.request.urlopen(url, timeout=10) as response:
                status = response.getcode()
                content = response.read().decode('utf-8')[:500]
                
                print(f"Status: {status}")
                
                if status == 200:
                    # Verificar se é HTML ou JSON
                    if content.strip().startswith('<!doctype') or content.strip().startswith('<html'):
                        print("Tipo: HTML (Frontend)")
                        working_urls.append((name, url, "HTML"))
                    else:
                        try:
                            json.loads(content)
                            print("Tipo: JSON (API)")
                            working_urls.append((name, url, "JSON"))
                        except:
                            print("Tipo: Outro")
                            working_urls.append((name, url, "OUTRO"))
                    
                    print(f"✅ FUNCIONANDO")
                else:
                    print(f"❌ ERRO: {status}")
                    broken_urls.append((name, url, status))
                
                print(f"Conteúdo: {content[:100]}...")
                print()
                
        except Exception as e:
            print(f"❌ ERRO: {e}")
            broken_urls.append((name, url, str(e)))
            print()
    
    # Resumo
    print("=== RESUMO ===")
    print()
    print("✅ URLs FUNCIONANDO:")
    for name, url, tipo in working_urls:
        print(f"   {name}: {url} ({tipo})")
    
    print()
    print("❌ URLs COM ERRO:")
    for name, url, error in broken_urls:
        print(f"   {name}: {url} ({error})")
    
    print()
    print("=== ANÁLISE ===")
    
    # Análise automática
    frontend_working = any("Frontend" in name and url.endswith("vercel.app") for name, url, _ in working_urls)
    backend_vercel_working = any("Backend" in name and "vercel.app" in url and tipo == "JSON" for name, url, tipo in working_urls)
    backend_render_working = any("Backend" in name and "onrender.com" in url for name, url, _ in working_urls)
    
    print(f"Frontend Vercel: {'✅' if frontend_working else '❌'}")
    print(f"Backend Vercel: {'✅' if backend_vercel_working else '❌'}")
    print(f"Backend Render: {'✅' if backend_render_working else '❌'}")
    
    print()
    print("=== RECOMENDAÇÕES ===")
    
    if frontend_working and backend_vercel_working:
        print("✅ SISTEMA COMPLETO FUNCIONANDO!")
        print("   Acesse: https://chama-o-mika.vercel.app/login")
        print("   Use: admin/mika123")
    elif frontend_working and not backend_vercel_working:
        print("⚠️ Frontend funciona mas backend não")
        print("   Verifique se o backend foi implantado corretamente")
    elif not frontend_working:
        print("❌ Frontend não está funcionando")
        print("   Verifique o deploy do frontend")
    
    if backend_render_working:
        print("⚠️ Backend Render está ativo")
        print("   Mas você deveria usar o backend Vercel")
        print("   URL correta: https://chama-o-mika.vercel.app/api")

if __name__ == '__main__':
    debug_deploy()
