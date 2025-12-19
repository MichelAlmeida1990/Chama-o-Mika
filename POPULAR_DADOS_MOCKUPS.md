# 📊 Como Popular o Sistema com Dados Mockups

Este guia explica como popular o sistema com dados de exemplo (categorias, produtos, clientes e vendas) para testar os dashboards e métricas.

## 🎯 O que será criado

- **7 Categorias**: Camisetas, Calças, Vestidos, Shorts, Blusas, Saias, Acessórios
- **20 Produtos**: Variados com diferentes tamanhos, cores e preços
- **8 Clientes**: Com dados completos
- **30-90 Vendas**: Distribuídas nos últimos 30 dias (1-3 vendas por dia)

## 🚀 Método 1: Via Endpoint HTTP (Recomendado para Render)

### 1. Configurar Secret (Opcional mas Recomendado)

No **Render Dashboard** → **Settings** → **Environment Variables**:

Adicione:
- **Nome**: `POPULATE_SECRET`
- **Valor**: `sua-chave-secreta-aqui` (ex: `populate123`)

### 2. Chamar o Endpoint

**Opção A - Com Secret (Recomendado):**

```bash
curl -X POST https://seu-backend.onrender.com/api/populate-mock-data/ \
  -H "X-Populate-Secret: sua-chave-secreta-aqui" \
  -H "Content-Type: application/json"
```

**Opção B - Sem Secret (se não configurou):**

```bash
curl -X POST https://seu-backend.onrender.com/api/populate-mock-data/
```

**Opção C - Via Navegador (Postman/Insomnia):**

- **URL**: `https://seu-backend.onrender.com/api/populate-mock-data/`
- **Método**: `POST`
- **Headers**: 
  - `X-Populate-Secret: sua-chave-secreta-aqui` (se configurou)
- **Body**: Vazio

### 3. Resposta Esperada

```json
{
  "success": true,
  "message": "Dados mockups criados com sucesso!",
  "output": "🚀 Iniciando população de dados mockups...\n..."
}
```

## 🖥️ Método 2: Via Management Command (Local ou Shell)

Se você tiver acesso ao shell do Render (pago) ou estiver rodando localmente:

```bash
python manage.py populate_mock_data
```

### Opções do Comando

```bash
# Popular dados (mantém dados existentes)
python manage.py populate_mock_data

# Limpar e popular (remove dados existentes primeiro)
python manage.py populate_mock_data --clear
```

## 📊 Verificar os Dados

Após popular, você pode verificar:

1. **Dashboard**: Acesse o frontend e veja os gráficos e métricas
2. **Admin**: `https://seu-backend.onrender.com/admin/`
   - Estoque → Produtos
   - Financeiro → Clientes
   - Financeiro → Vendas

## 🔍 O que será criado

### Categorias
- Camisetas
- Calças
- Vestidos
- Shorts
- Blusas
- Saias
- Acessórios

### Produtos
- 20 produtos variados
- Alguns com estoque baixo (para testar alertas)
- Preços de custo e venda configurados

### Clientes
- 8 clientes com dados completos
- CPF, email, telefone, endereço

### Vendas
- 30-90 vendas (1-3 por dia)
- Distribuídas nos últimos 30 dias
- Com itens variados
- Algumas com desconto (10% das vendas)
- Status: CONCLUIDA
- Estoque atualizado automaticamente

## ⚠️ Importante

- **Este endpoint é temporário** - considere removê-lo após popular os dados
- **Use o secret** para proteger o endpoint em produção
- **Os dados são realistas** mas são apenas para teste
- **As vendas atualizam o estoque** automaticamente

## 🗑️ Limpar Dados

Para limpar e recriar:

**Via Endpoint:**
```bash
# Não há opção --clear via endpoint, use o comando ou delete manualmente
```

**Via Admin:**
- Acesse o Django Admin
- Delete manualmente as vendas, clientes, produtos e categorias

**Via Shell:**
```bash
python manage.py populate_mock_data --clear
```

## ✅ Próximos Passos

Após popular os dados:

1. ✅ Acesse o dashboard e verifique os gráficos
2. ✅ Verifique as métricas financeiras
3. ✅ Teste os relatórios
4. ✅ Verifique os alertas de estoque baixo
5. ✅ Teste a criação de novas vendas

## 🔒 Segurança

Após popular os dados, considere:

1. **Remover o endpoint** se não precisar mais
2. **Ou manter o secret** bem protegido
3. **Ou desabilitar** o endpoint em produção

Para desabilitar, remova a linha do `urls.py`:
```python
path('api/populate-mock-data/', populate_mock_data_view, name='populate_mock_data'),
```

