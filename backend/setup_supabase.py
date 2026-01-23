"""
Script para configurar Supabase como banco de dados externo e persistente
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def setup_supabase():
    """Configurar Supabase como banco de dados persistente"""
    
    print("=== CONFIGURAÇÃO SUPABASE PARA SMARTMANAGER ===\n")
    
    print("📋 OPÇÕES DE BANCO DE DADOS EXTERNO GRATUITO:\n")
    
    print("1. 🟢 SUPABASE (RECOMENDADO)")
    print("   ✅ Gratuito e generoso")
    print("   ✅ PostgreSQL completo")
    print("   ✅ Interface web amigável")
    print("   ✅ API REST automática")
    print("   ✅ Autenticação integrada")
    print("   ✅ Persistência garantida")
    print("   ✅ Fácil configuração")
    print("   ✅ Backup automático")
    print()
    
    print("2. 🟡 PLANETSCALE")
    print("   ✅ MySQL compatível")
    print("   ✅ Escalável")
    print("   ❌ Configuração mais complexa")
    print()
    
    print("3. 🟡 RAILWAY")
    print("   ✅ PostgreSQL")
    print("   ✅ Simples")
    print("   ❌ Limites mais restritivos")
    print()
    
    print("🚀 CONFIGURANDO SUPABASE:\n")
    
    print("PASSO 1: Criar conta Supabase")
    print("   1. Acesse: https://supabase.com")
    print("   2. Clique em 'Start your project'")
    print("   3. Use GitHub/Google para login")
    print("   4. Crie novo projeto:")
    print("      - Nome: smartmanager-db")
    print("      - Senha: gere uma senha forte")
    print("      - Região: escolha a mais próxima")
    print()
    
    print("PASSO 2: Obter credenciais")
    print("   1. Aguarde criação (2-3 minutos)")
    print("   2. Vá para Settings > Database")
    print("   3. Copie a 'Connection string'")
    print("   4. Formato: postgresql://user:pass@host:port/dbname")
    print()
    
    print("PASSO 3: Configurar no deploy")
    print("   1. No Vercel, adicione variável de ambiente:")
    print("      DATABASE_URL=postgresql://user:pass@host:port/dbname")
    print("   2. Faça deploy")
    print("   3. Pronto! Dados persistirão automaticamente")
    print()
    
    print("📝 VANTAGENS DO SUPABASE:")
    print("   • 500MB de armazenamento gratuito")
    print("   • 50.000 autenticações/mês")
    print("   • 2GB de transferência")
    print("   • Backup automático diário")
    print("   • Dashboard completo")
    print("   • API REST automática")
    print("   • Real-time subscriptions")
    print()
    
    print("🔧 CONFIGURAÇÃO TÉCNICA:")
    print("   • O sistema já detecta DATABASE_URL automaticamente")
    print("   • Migrações rodam automaticamente no deploy")
    print("   • Usuários são criados via script ou admin")
    print("   • Dados persistem entre deploys")
    print()
    
    print("⚡ ALTERNATIVA RÁPIDA:")
    print("   Se quiser testar sem configurar:")
    print("   • Use Railway: https://railway.app")
    print("   • Conecte GitHub")
    print("   • Add PostgreSQL service")
    print("   • Copie DATABASE_URL")
    print()
    
    print("🎯 RECOMENDAÇÃO FINAL:")
    print("   Use Supabase - é gratuito, robusto e perfeito para o SmartManager!")
    
    return True

if __name__ == '__main__':
    setup_supabase()
