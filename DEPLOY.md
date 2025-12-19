# 🚀 Guia de Deploy - Chama o Mika

Este guia explica como fazer o deploy do sistema **Chama o Mika** no **Render** (backend) e **Vercel** (frontend).

## 📋 Pré-requisitos

- Conta no [Render](https://render.com)
- Conta no [Vercel](https://vercel.com)
- Repositório Git (GitHub, GitLab ou Bitbucket)
- Código do projeto commitado e enviado para o repositório

---

## 🔧 Deploy do Backend (Render)

### 1. Preparação

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **New +** → **Web Service**
3. Conecte seu repositório Git

### 2. Configurações do Serviço

**Configurações Básicas:**
- **Name**: `chama-o-mika-backend` (ou o nome que preferir)
- **Environment**: `Python 3`
- **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
- **Start Command**: `cd backend && gunicorn gestao.wsgi:application --bind 0.0.0.0:$PORT`

**Variáveis de Ambiente:**
Adicione as seguintes variáveis de ambiente no painel do Render:

```env
SECRET_KEY=gerar-uma-chave-secreta-forte-aqui
DEBUG=False
ALLOWED_HOSTS=seu-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
SECURE_SSL_REDIRECT=True
```

**Para gerar uma SECRET_KEY segura:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Banco de Dados (Opcional mas Recomendado)

1. No Render Dashboard, clique em **New +** → **PostgreSQL**
2. Configure o banco de dados
3. Copie a **Internal Database URL**
4. Adicione como variável de ambiente `DATABASE_URL` no seu Web Service
5. Atualize o `settings.py` para usar PostgreSQL em produção:

```python
import dj_database_url

# No settings.py, substitua a configuração de DATABASES por:
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

E adicione `dj-database-url==2.1.0` ao `requirements.txt`.

### 4. Deploy

1. Clique em **Create Web Service**
2. Aguarde o build e deploy
3. Anote a URL do serviço (ex: `https://chama-o-mika-backend.onrender.com`)

### 5. Criar Superusuário

Após o deploy, acesse o terminal do Render e execute:

```bash
cd backend
python manage.py createsuperuser
```

Ou use o script:

```bash
cd backend
python manage.py shell -c "exec(open('create_superuser.py').read())"
```

---

## 🎨 Deploy do Frontend (Vercel)

### 1. Preparação

1. Acesse [Vercel Dashboard](https://vercel.com/dashboard)
2. Clique em **Add New** → **Project**
3. Conecte seu repositório Git

### 2. Configurações do Projeto

**Configurações Básicas:**
- **Framework Preset**: `Create React App`
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

**Variáveis de Ambiente:**
Adicione a seguinte variável de ambiente:

```env
REACT_APP_API_URL=https://seu-backend.onrender.com
```

**⚠️ IMPORTANTE:** Substitua `seu-backend.onrender.com` pela URL real do seu backend no Render.

### 3. Deploy

1. Clique em **Deploy**
2. Aguarde o build e deploy
3. Anote a URL do frontend (ex: `https://chama-o-mika.vercel.app`)

### 4. Atualizar CORS no Backend

Após obter a URL do frontend, volte ao Render e atualize a variável de ambiente:

```env
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

E reinicie o serviço no Render.

---

## 🔄 Atualizações Futuras

### Backend (Render)
- Push para o repositório Git automaticamente faz deploy
- Ou use o botão **Manual Deploy** no dashboard

### Frontend (Vercel)
- Push para o repositório Git automaticamente faz deploy
- Ou use o botão **Redeploy** no dashboard

---

## 🧪 Testando o Deploy

1. Acesse a URL do frontend no Vercel
2. Tente fazer login com as credenciais do superusuário criado
3. Verifique se todas as funcionalidades estão funcionando

---

## 🐛 Troubleshooting

### Backend não inicia
- Verifique os logs no Render Dashboard
- Confirme que todas as variáveis de ambiente estão configuradas
- Verifique se o `Start Command` está correto

### Frontend não conecta ao Backend
- Verifique se `REACT_APP_API_URL` está configurada corretamente
- Confirme que `CORS_ALLOWED_ORIGINS` inclui a URL do frontend
- Verifique os logs do navegador (F12 → Console)

### Erro 500 no Backend
- Verifique os logs no Render Dashboard
- Confirme que as migrações foram executadas
- Verifique se o banco de dados está configurado corretamente

### Erro de CORS
- Confirme que a URL do frontend está em `CORS_ALLOWED_ORIGINS`
- Verifique se `CORS_ALLOW_CREDENTIALS` está como `True`
- Reinicie o serviço após alterar variáveis de ambiente

---

## 📝 Checklist de Deploy

### Backend (Render)
- [ ] Serviço criado e configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Build Command configurado
- [ ] Start Command configurado
- [ ] Banco de dados configurado (opcional)
- [ ] Superusuário criado
- [ ] URL do backend anotada

### Frontend (Vercel)
- [ ] Projeto criado e configurado
- [ ] Root Directory configurado como `frontend`
- [ ] Variável `REACT_APP_API_URL` configurada
- [ ] Deploy realizado com sucesso
- [ ] URL do frontend anotada

### Pós-Deploy
- [ ] CORS atualizado no backend com URL do frontend
- [ ] Backend reiniciado após atualizar CORS
- [ ] Login testado
- [ ] Funcionalidades principais testadas

---

## 🔐 Segurança

- ✅ Nunca commite arquivos `.env` no Git
- ✅ Use `SECRET_KEY` forte e única
- ✅ Mantenha `DEBUG=False` em produção
- ✅ Configure `ALLOWED_HOSTS` corretamente
- ✅ Use HTTPS (Render e Vercel fornecem automaticamente)

---

## 📚 Recursos Adicionais

- [Documentação Render](https://render.com/docs)
- [Documentação Vercel](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

**Boa sorte com o deploy! 🚀**

