# 🔧 Solução: Erro "Secret inválido" no Endpoint de Populate

## ❌ Problema

Ao chamar o endpoint `/api/populate-mock-data/`, você recebe:
```json
{"error": "Secret inválido"}
```

## 🔍 Causa

A variável de ambiente `POPULATE_SECRET` está configurada no Render, mas você não está enviando o secret na requisição.

## ✅ Soluções

### Solução 1: Remover o Secret (Mais Simples)

Se você não precisa de proteção extra, **remova a variável de ambiente**:

1. **Render Dashboard** → **Settings** → **Environment Variables**
2. Encontre `POPULATE_SECRET`
3. **Delete** a variável
4. **Salve** e aguarde o restart
5. Chame o endpoint novamente:
   ```bash
   curl -X POST https://chama-o-mika-backend.onrender.com/api/populate-mock-data/
   ```

### Solução 2: Enviar o Secret na Requisição

Se você quer manter o secret por segurança, envie-o na requisição:

**Opção A - Via Header:**
```bash
curl -X POST https://chama-o-mika-backend.onrender.com/api/populate-mock-data/ \
  -H "X-Populate-Secret: seu-secret-aqui"
```

**Opção B - Via Query String:**
```bash
curl -X POST "https://chama-o-mika-backend.onrender.com/api/populate-mock-data/?secret=seu-secret-aqui"
```

**Opção C - Via Postman/Insomnia:**
- **URL**: `https://chama-o-mika-backend.onrender.com/api/populate-mock-data/`
- **Método**: `POST`
- **Headers**: 
  - `X-Populate-Secret: seu-secret-aqui`
- **Body**: Vazio

### Solução 3: Verificar o Secret Configurado

Para ver qual secret está configurado:

1. **Render Dashboard** → **Settings** → **Environment Variables**
2. Procure por `POPULATE_SECRET`
3. Copie o valor
4. Use esse valor na requisição

## 🎯 Recomendação

**Para desenvolvimento/teste**: Use a **Solução 1** (remover o secret)

**Para produção**: Use a **Solução 2** (manter o secret e enviá-lo)

## 📝 Nota

O endpoint foi atualizado para aceitar o secret via:
- Header: `X-Populate-Secret`
- Query String: `?secret=valor`
- POST body: `secret=valor`

Se `POPULATE_SECRET` não estiver configurado, o endpoint funciona **sem autenticação**.

