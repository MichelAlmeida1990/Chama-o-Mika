# 🔐 Credenciais e Variáveis de Ambiente - Chama o Mika

Documento com todas as variáveis de ambiente e credenciais necessárias.

---

## ⚠️ SEGURANÇA

**NUNCA** commite arquivos `.env` ou este documento com valores reais no Git!

---

## 📋 VARIÁVEIS DE AMBIENTE - BACKEND (RENDER)

Configure estas variáveis no **Render Dashboard → Environment Variables**

| Nome da Variável | Valor | Descrição |
|------------------|-------|-----------|
| `SECRET_KEY` | `6i!i#pr2ijih2eo6ne!^f=uq(hsbqi^hd7x*ef6_ver^#s!qvu` | Chave secreta do Django (gerar nova para produção) |
| `DEBUG` | `False` | Modo debug (sempre False em produção) |
| `ALLOWED_HOSTS` | `seu-backend.onrender.com,localhost,127.0.0.1` | Domínios permitidos (substituir pelo seu domínio) |
| `CORS_ALLOWED_ORIGINS` | `https://seu-frontend.vercel.app,http://localhost:3000` | URLs do frontend (substituir pela URL do Vercel) |
| `SECURE_SSL_REDIRECT` | `True` | Forçar HTTPS (True em produção) |
| `DATABASE_URL` | `postgresql://user:pass@host:port/dbname` | URL do PostgreSQL (fornecida pelo Render) |
| `AUTO_CREATE_SUPERUSER` | `True` | Cria automaticamente superusuário padrão (admin/admin123) se não existir |
| `MAKE_SUPERUSER` | `rafael@chamaomika.com` | Torna usuário existente superusuário automaticamente (use o email) |

### Como gerar SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Exemplo gerado:**
```
6i!i#pr2ijih2eo6ne!^f=uq(hsbqi^hd7x*ef6_ver^#s!qvu
```

⚠️ **IMPORTANTE**: Gere uma nova chave para produção!

---

## 🎨 VARIÁVEIS DE AMBIENTE - FRONTEND (VERCEL)

Configure esta variável no **Vercel Dashboard → Settings → Environment Variables**

| Nome da Variável | Valor | Descrição |
|------------------|-------|-----------|
| `REACT_APP_API_URL` | `https://seu-backend.onrender.com` | URL do backend (substituir pela URL do Render) |

**Exemplo:**
```
REACT_APP_API_URL = https://chama-o-mika-backend.onrender.com
```

---

## 🗄️ BANCO DE DADOS - POSTGRESQL (RENDER)

### Credenciais Automáticas

Quando você cria um PostgreSQL no Render, as credenciais são geradas automaticamente.

**Como obter:**

1. Render Dashboard → Seu serviço PostgreSQL
2. Seção **Connections**
3. Copie a **Internal Database URL** ou **External Database URL**

**Formato da URL:**
```
postgresql://usuario:senha@host:porta/banco
```

**Exemplo:**
```
postgresql://chama_mika_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com:5432/chama_mika_db
```

**Onde usar:**
- Cole esta URL completa como valor da variável `DATABASE_URL` no Render

⚠️ **IMPORTANTE**: 
- A senha é gerada automaticamente pelo Render
- Você não precisa configurar usuário/senha separadamente
- Use a URL completa como `DATABASE_URL`

---

## 👤 CREDENCIAIS DE ACESSO AO SISTEMA

### Superusuário (Admin)

Após o deploy, crie um superusuário para acessar o sistema.

**Como criar:**

**Opção 1 - Via Terminal do Render:**
```bash
cd backend
python manage.py createsuperuser
```

**Opção 2 - Via Script (credenciais padrão):**
```bash
cd backend
python manage.py shell -c "exec(open('create_superuser.py').read())"
```

### Credenciais Padrão (se usar o script):

| Campo | Valor |
|-------|-------|
| **Usuário** | `admin` |
| **Email** | `admin@example.com` |
| **Senha** | `admin123` |

⚠️ **IMPORTANTE**: 
- Altere a senha após o primeiro login!
- Use uma senha forte em produção
- Não compartilhe essas credenciais

---

## 📝 EXEMPLO COMPLETO - BACKEND (RENDER)

Aqui está um exemplo de como devem ficar as variáveis no Render:

```
SECRET_KEY = 6i!i#pr2ijih2eo6ne!^f=uq(hsbqi^hd7x*ef6_ver^#s!qvu
DEBUG = False
ALLOWED_HOSTS = chama-o-mika-backend.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = https://chama-o-mika.vercel.app,http://localhost:3000
SECURE_SSL_REDIRECT = True
DATABASE_URL = postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/chama_mika_db
```

**Substituir:**
- `chama-o-mika-backend.onrender.com` → Seu domínio do Render
- `https://chama-o-mika.vercel.app` → Sua URL do Vercel
- `postgresql://...` → Sua URL do PostgreSQL do Render

---

## 📝 EXEMPLO COMPLETO - FRONTEND (VERCEL)

Aqui está um exemplo de como deve ficar a variável no Vercel:

```
REACT_APP_API_URL = https://chama-o-mika-backend.onrender.com
```

**Substituir:**
- `https://chama-o-mika-backend.onrender.com` → URL do seu backend no Render

---

## 🔄 ORDEM DE CONFIGURAÇÃO

### 1️⃣ Backend (Render)

Configure estas variáveis:
- ✅ `SECRET_KEY` (gerar nova)
- ✅ `DEBUG = False`
- ✅ `ALLOWED_HOSTS` (com seu domínio do Render)
- ✅ `SECURE_SSL_REDIRECT = True`
- ✅ `DATABASE_URL` (se usar PostgreSQL)
- ⏳ `CORS_ALLOWED_ORIGINS` (atualizar depois com URL do frontend)

Faça o deploy e anote a URL do backend.

### 2️⃣ Frontend (Vercel)

Configure esta variável:
- ✅ `REACT_APP_API_URL` (com a URL do backend do Render)

Faça o deploy e anote a URL do frontend.

### 3️⃣ Atualizar CORS

Volte ao Render e atualize:
- ✅ `CORS_ALLOWED_ORIGINS` (adicione a URL do frontend do Vercel)

Reinicie o serviço no Render.

---

## 🛠️ COMANDOS ÚTEIS

### Gerar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Criar Superusuário
```bash
cd backend
python manage.py createsuperuser
```

### Verificar Variáveis (Django Shell)
```bash
cd backend
python manage.py shell
>>> import os
>>> print(os.environ.get('SECRET_KEY'))
>>> print(os.environ.get('DEBUG'))
```

---

## ✅ CHECKLIST RÁPIDO

### Backend (Render)
- [ ] `SECRET_KEY` gerada e configurada
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` com domínio do Render
- [ ] `CORS_ALLOWED_ORIGINS` (atualizar após deploy do frontend)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `DATABASE_URL` configurada (se usar PostgreSQL)
- [ ] Superusuário criado

### Frontend (Vercel)
- [ ] `REACT_APP_API_URL` com URL do backend configurada

---

## 🔒 BOAS PRÁTICAS

1. ✅ **Nunca** commite arquivos `.env` no Git
2. ✅ Use senhas fortes e únicas
3. ✅ Gere nova `SECRET_KEY` para cada ambiente
4. ✅ Mantenha `DEBUG=False` em produção
5. ✅ Configure `ALLOWED_HOSTS` corretamente
6. ✅ Altere credenciais padrão após primeiro acesso
7. ✅ Guarde credenciais em local seguro

---

## 🆘 PROBLEMAS COMUNS

### Erro: "Invalid SECRET_KEY"
- Gere uma nova chave usando o comando acima
- Certifique-se de que não há espaços extras

### Erro: "DisallowedHost"
- Verifique se o domínio está em `ALLOWED_HOSTS`
- Certifique-se de que não há espaços extras na lista

### Erro: CORS bloqueado
- Verifique se a URL do frontend está em `CORS_ALLOWED_ORIGINS`
- Certifique-se de que não há espaços extras
- Reinicie o serviço após alterar

### Erro: Não conecta ao banco
- Verifique se `DATABASE_URL` está correta
- Certifique-se de que o banco está ativo no Render
- Use a URL interna ou externa correta

---

**Última atualização**: Dezembro 2024
