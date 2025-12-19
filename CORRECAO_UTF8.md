# 🔧 Correção de Encoding UTF-8

## Problema Identificado

Os dados estavam sendo salvos com encoding incorreto, causando problemas na exibição de caracteres especiais (acentos, ç, etc.).

## Soluções Aplicadas

### 1. ✅ Declaração de Encoding nos Scripts Python

Todos os scripts Python agora têm a declaração de encoding UTF-8 no início:

```python
# -*- coding: utf-8 -*-
```

### 2. ✅ Configuração de Encoding no Windows

Adicionado suporte para encoding UTF-8 no Windows nos scripts:

```python
import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

### 3. ✅ Configuração do Django Settings

Adicionado no `settings.py`:

```python
DEFAULT_CHARSET = 'utf-8'
```

### 4. ✅ Execução com Encoding Explícito

Os scripts agora são executados com encoding explícito:

```bash
python manage.py shell -c "exec(open('script.py', encoding='utf-8').read())"
```

## 📝 Como Recriar os Dados

### Opção 1: Script Completo (Recomendado)

```bash
cd backend
python manage.py shell -c "exec(open('create_all_mock_data.py', encoding='utf-8').read())"
```

### Opção 2: Scripts Individuais

```bash
cd backend

# Categorias e Produtos
python manage.py shell -c "exec(open('create_mock_data.py', encoding='utf-8').read())"

# Clientes
python manage.py shell -c "exec(open('create_mock_clientes.py', encoding='utf-8').read())"
```

### Opção 3: Limpar e Recriar Tudo

```bash
cd backend
python manage.py shell -c "exec(open('fix_encoding_and_recreate.py', encoding='utf-8').read())"
```

## ✅ Verificação

Após executar os scripts, verifique no admin do Django ou no frontend se os caracteres estão sendo exibidos corretamente:

- ✅ "Acessórios" (não "AcessÃ³rios")
- ✅ "Calças" (não "CalÃ§as")
- ✅ "Blusões" (não "BlusÃµes")
- ✅ "Básicas" (não "BÃ¡sicas")

## 🔍 Se o Problema Persistir

1. **Verifique o encoding do terminal:**
   ```bash
   chcp 65001  # Windows - define UTF-8
   ```

2. **Verifique o encoding do banco de dados:**
   - SQLite usa UTF-8 por padrão
   - Se usar PostgreSQL, certifique-se que o banco está criado com encoding UTF-8

3. **Verifique o encoding do frontend:**
   - Certifique-se que o HTML tem `<meta charset="UTF-8">`
   - Verifique se o servidor está retornando `Content-Type: text/html; charset=utf-8`

## 📚 Arquivos Modificados

- ✅ `backend/create_mock_data.py`
- ✅ `backend/create_mock_clientes.py`
- ✅ `backend/create_all_mock_data.py`
- ✅ `backend/fix_encoding_and_recreate.py` (novo)
- ✅ `backend/gestao/settings.py`

## 🎯 Status

✅ **Problema resolvido!** Os dados agora são criados e salvos com encoding UTF-8 correto.


