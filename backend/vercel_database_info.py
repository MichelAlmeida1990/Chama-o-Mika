"""
Configuração para banco de dados persistente no Vercel
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

def setup_vercel_database():
    """Configurar banco de dados persistente no Vercel"""
    
    print("=== BANCO DE DADOS PERSISTENTE NO VERCEL ===\n")
    
    print("🔍 SITUAÇÃO ATUAL:")
    print("   • Deploy: Vercel (Serverless)")
    print("   • Backend: Django + @vercel/python")
    print("   • Banco: SQLite (padrão) - NÃO PERSISTENTE")
    print("   • Problema: Dados perdidos a cada deploy")
    print()
    
    print("🚨 PROBLEMA IDENTIFICADO:")
    print("   Vercel é serverless - não armazena arquivos permanentemente")
    print("   SQLite é um arquivo local - perdido a cada deploy")
    print("   Precisamos de banco externo ou persistência")
    print()
    
    print("💡 SOLUÇÕES DISPONÍVEIS:")
    print()
    
    print("1. 🟢 VERCEL KV (RECOMENDADO)")
    print("   ✅ Integrado ao Vercel")
    print("   ✅ Gratuito (10k comandos/dia)")
    print("   ✅ Persistente")
    print("   ❌ Redis (não SQL)")
    print("   ❌ Requer adaptação do código")
    print()
    
    print("2. 🟡 VERCEL POSTGRES")
    print("   ✅ PostgreSQL nativo")
    print("   ✅ Persistente")
    print("   ✅ SQL completo")
    print("   ❌ Plano pago ($20/mês)")
    print("   ✅ Melhor opção se pagar")
    print()
    
    print("3. 🟠 UPSTASH REDIS")
    print("   ✅ Gratuito generoso")
    print("   ✅ Persistente")
    print("   ❌ Redis (não SQL)")
    print("   ❌ Requer adaptação")
    print()
    
    print("4. 🔴 SQLITE + VERCEL BLOB (NÃO RECOMENDADO)")
    print("   ❌ Complexo")
    print("   ❌ Performance ruim")
    print("   ❌ Possível corrupção")
    print()
    
    print("🎯 RECOMENDAÇÃO:")
    print()
    
    print("OPÇÃO A - VERCEL POSTGRES (PAGO):")
    print("   1. Dashboard Vercel → Storage → Create Database")
    print("   2. Escolher PostgreSQL")
    print("   3. Copiar DATABASE_URL")
    print("   4. Adicionar variável de ambiente")
    print("   5. Deploy - dados persistirão!")
    print()
    
    print("OPÇÃO B - MANTER SQLITE + BACKUP:")
    print("   1. Criar endpoint de backup")
    print("   2. Salvar dados em JSON periodicamente")
    print("   3. Restaurar após deploy")
    print("   ❌ Complexo e frágil")
    print()
    
    print("OPÇÃO C - MIGRAR PARA RENDER:")
    print("   1. Mudar backend para Render")
    print("   2. PostgreSQL gratuito")
    print("   3. Frontend continua no Vercel")
    print("   ✅ Solução mais robusta")
    print()
    
    print("🔧 CONFIGURAÇÃO ATUAL:")
    print("   O código já suporta DATABASE_URL")
    print("   Basta adicionar variável de ambiente")
    print("   Migrações rodam automaticamente")
    print()
    
    print("📊 COMPARATIVO:")
    print("   Serviço      | Custo   | Persistência | Setup")
    print("   Vercel KV    | Grátis  | ✅          | Médio")
    print("   Vercel PG    | $20/mês | ✅          | Fácil")
    print("   Render       | Grátis  | ✅          | Fácil")
    print("   SQLite       | Grátis  | ❌          | Fácil")
    print()
    
    print("🎯 DECISÃO:")
    print("   Para persistência real sem config externa:")
    print("   → Vercel Postgres (paga mas fácil)")
    print("   → Render (grátis mas migra backend)")
    print()
    
    print("Qual opção prefere?")

if __name__ == '__main__':
    setup_vercel_database()
