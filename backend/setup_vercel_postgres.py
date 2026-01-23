"""
Configuração Vercel Postgres para SmartManager
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

def setup_vercel_postgres():
    """Configurar Vercel Postgres para persistência de dados"""
    
    print("=== CONFIGURAÇÃO VERCEL POSTGRES ===\n")
    
    print("🚀 PASSO A PASSO - VERCEL POSTGRES:\n")
    
    print("1. 📋 CRIAR BANCO DE DADOS")
    print("   1. Acesse: https://vercel.com/dashboard")
    print("   2. Vá para seu projeto: smartmanager")
    print("   3. Clique em 'Storage' no menu lateral")
    print("   4. Clique em 'Create Database'")
    print("   5. Escolha 'Postgres'")
    print("   6. Configure:")
    print("      - Database Name: smartmanager-db")
    print("      - Region: escolha a mais próxima (ex: Washington D.C.)")
    print("   7. Clique em 'Create'")
    print()
    
    print("2. 🔗 OBTER CONNECTION STRING")
    print("   1. Após criação, vá para Settings do banco")
    print("   2. Copie 'Connection String'")
    print("   3. Formato: postgresql://user:password@host:port/dbname")
    print()
    
    print("3. ⚙️ CONFIGURAR VARIÁVEIS DE AMBIENTE")
    print("   1. No projeto Vercel, vá para Settings → Environment Variables")
    print("   2. Adicione:")
    print("      - Name: DATABASE_URL")
    print("      - Value: cole a connection string")
    print("      - Environments: Production, Preview, Development")
    print("   3. Clique em 'Save'")
    print()
    
    print("4. 🔄 FAZER DEPLOY")
    print("   1. Commit e push das mudanças")
    print("   2. Aguarde o deploy automático")
    print("   3. O sistema detectará DATABASE_URL automaticamente")
    print("   4. Migrações rodarão automaticamente")
    print()
    
    print("5. 👥 CRIAR USUÁRIOS")
    print("   Após o deploy, crie usuários:")
    print("   - Opção A: Via admin")
    print("   - Opção B: Via script (já configurado)")
    print()
    
    print("✅ VANTAGENS:")
    print("   • Dados 100% persistentes")
    print("   • PostgreSQL completo")
    print("   • Backup automático")
    print("   • Escalável")
    print("   • Integrado ao Vercel")
    print()
    
    print("💰 CUSTO:")
    print("   • Plano Hobby: $20/mês")
    print("   • Inclui:")
    print("     - 8GB storage")
    print("     - 60GB transferência/mês")
    print("     - 3 conexões simultâneas")
    print("     - Backup automático")
    print()
    
    print("🔧 CONFIGURAÇÃO TÉCNICA:")
    print("   • O settings.py já detecta DATABASE_URL")
    print("   • dj-database-url já instalado")
    print("   • Migrações automáticas no deploy")
    print("   • Sem mudanças no código necessárias")
    print()
    
    print("📋 CHECKLIST PÓS-CONFIGURAÇÃO:")
    print("   [ ] Banco criado no Vercel")
    print("   [ ] DATABASE_URL configurada")
    print("   [ ] Deploy realizado")
    print("   [ ] Migrações aplicadas")
    print("   [ ] Usuários criados")
    print("   [ ] Login funcionando")
    print("   [ ] Dados persistindo")
    print()
    
    print("🎯 PRÓXIMOS PASSOS:")
    print("   1. Siga os passos acima")
    print("   2. Me avise quando configurar")
    print("   3. Ajudarei a verificar se está funcionando")
    print()
    
    return True

def verify_postgres_setup():
    """Verificar se PostgreSQL está configurado"""
    
    print("=== VERIFICAÇÃO POSTGRES ===\n")
    
    # Verificar configuração atual
    database_url = os.environ.get('DATABASE_URL', '').strip()
    
    if database_url and database_url.startswith('postgresql://'):
        print("✅ DATABASE_URL detectada:")
        print(f"   {database_url[:50]}...")
        
        try:
            import dj_database_url
            db_config = dj_database_url.parse(database_url)
            print(f"   Host: {db_config['HOST']}")
            print(f"   Port: {db_config['PORT']}")
            print(f"   Database: {db_config['NAME']}")
            print("✅ Configuração PostgreSQL válida!")
        except Exception as e:
            print(f"❌ Erro na configuração: {e}")
    else:
        print("❌ DATABASE_URL não configurada ou não é PostgreSQL")
        print("   Configure no Vercel: Settings → Environment Variables")
    
    return database_url.startswith('postgresql://') if database_url else False

if __name__ == '__main__':
    setup_vercel_postgres()
    print("\n" + "="*50)
    verify_postgres_setup()
