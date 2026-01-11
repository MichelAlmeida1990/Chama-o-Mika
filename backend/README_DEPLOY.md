# Deploy - Usuários e Autenticação

## Problema Resolvido

O erro "usuário ou senha inválidos" no deploy foi causado por:
1. Senhas não sincronizadas entre ambiente local e deploy
2. Validação de senha do Django bloqueando criação/atualização

## Solução

### 1. Script de Deploy Simplificado

Execute no servidor de deploy:
```bash
cd /path/to/deploy/backend
python deploy_users_simple.py
```

### 2. Credenciais Válidas

| Usuário | Senha | Status |
|---------|--------|---------|
| admin | mika123 | ✅ Testado |
| mika | mika123 | ✅ Testado |
| rafael@chamaomika.com | mika123 | ✅ Testado |

### 3. Verificação Manual

Se preferir verificar manualmente:

1. **Acessar Admin do Deploy:**
   ```
   https://seu-deploy.com/admin/
   ```

2. **Verificar Usuários:**
   - Authentication and Authorization → Users
   - Procure por: admin, mika, rafael@chamaomika.com

3. **Se não existirem, crie:**
   - Username: admin
   - Email: admin@chamaomika.com  
   - Password: mika123
   - Staff status: ✅
   - Superuser status: ✅

### 4. Teste de API

Teste a autenticação via API:
```bash
curl -X POST https://seu-deploy.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "mika123"}'
```

## Arquivos Importantes

- `deploy_users_simple.py` - Script para criar usuários no deploy
- `check_users.py` - Verificar usuários existentes
- `fix_users.py` - Corrigir senhas localmente

## Próximos Passos

1. ✅ Executar `deploy_users_simple.py` no servidor
2. ✅ Testar login no frontend do deploy
3. ✅ Verificar se categorias estão funcionando
4. ✅ Testar criação de produtos

## Suporte

Se o problema persistir:
1. Verifique as variáveis de ambiente do deploy
2. Confirme o banco de dados está correto
3. Verifique logs do servidor: `heroku logs --tail`
