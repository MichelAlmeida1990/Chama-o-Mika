# 🔧 CORRIGIR URL DA API NO FRONTEND

## Problema Identificado

❌ **URL Incorreta:** `chama-o-mika-backend.onrender.com`
✅ **URL Correta:** `https://chama-o-mika.vercel.app/api`

## 🚨 Erros no Console

1. **401 Unauthorized** - API não encontrada
2. **ERR_NAME_NOT_RESOLVED** - URL incorreta
3. **CSP Errors** - Scripts bloqueados

## ✅ Solução

### 1. Criar arquivo .env.production

**Crie o arquivo:** `c:\Projetos\Chama o Mika\frontend\.env.production`

**Conteúdo:**
```
# Ambiente de Produção - Vercel
REACT_APP_API_URL=https://chama-o-mika.vercel.app/api
```

### 2. Atualizar package.json

**Adicione os scripts:**
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "build:prod": "cp .env.production .env && react-scripts build"
  }
}
```

### 3. Fazer Deploy com Variável Correta

**Opção A - Vercel CLI:**
```bash
cd frontend
cp .env.production .env
npm run build
vercel --prod
```

**Opção B - GitHub Actions (se configurado):**
- O arquivo `.env.production` será usado automaticamente

## 📋 Verificação

Após corrigir:
1. **Build local:** `npm run build:prod`
2. **Verifique o build:** Deve usar a URL correta
3. **Faça deploy:** Teste no ambiente local primeiro

## 🎯 URLs Corretas

| Ambiente | URL da API |
|-----------|-------------|
| Desenvolvimento | http://localhost:8000 |
| Produção | https://chama-o-mika.vercel.app/api |

## ⚡ Ação Imediata

**Crie o arquivo .env.production com a URL correta!**

O frontend está tentando acessar o backend errado. Corrigindo isso, o login funcionará perfeitamente.
