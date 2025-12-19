# ✅ Checklist de Deploy - Chama o Mika

Use este checklist para garantir que tudo está pronto para o deploy.

## 📦 Preparação

### Backend
- [x] `requirements.txt` atualizado com todas as dependências
- [x] `settings.py` configurado para produção
- [x] `Procfile` criado para Render
- [x] `build.sh` criado (opcional)
- [x] WhiteNoise configurado para arquivos estáticos
- [x] Suporte a PostgreSQL via `dj-database-url`
- [x] Variáveis de ambiente configuráveis
- [x] CORS configurado dinamicamente

### Frontend
- [x] `package.json` com script `build`
- [x] `vercel.json` configurado
- [x] `api.js` usando variável de ambiente `REACT_APP_API_URL`
- [x] Build testado localmente ✅
- [x] Responsivo para mobile ✅

### Git
- [x] `.gitignore` configurado
- [x] Arquivos sensíveis não commitados (.env, db.sqlite3, etc)

---

## 🚀 Deploy no Render (Backend)

### Configuração Inicial
- [ ] Conta criada no Render
- [ ] Repositório conectado
- [ ] Web Service criado

### Variáveis de Ambiente
- [ ] `SECRET_KEY` configurada (gerar com Django)
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` com domínio do Render
- [ ] `CORS_ALLOWED_ORIGINS` (será atualizada após deploy do frontend)
- [ ] `SECURE_SSL_REDIRECT=True`

### Banco de Dados (Opcional)
- [ ] PostgreSQL criado no Render
- [ ] `DATABASE_URL` adicionada como variável de ambiente
- [ ] `dj-database-url` no requirements.txt ✅

### Build e Start Commands
- [ ] Build Command: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
- [ ] Start Command: `cd backend && gunicorn gestao.wsgi:application --bind 0.0.0.0:$PORT`

### Pós-Deploy
- [ ] Deploy concluído com sucesso
- [ ] URL do backend anotada: `https://________________.onrender.com`
- [ ] Superusuário criado
- [ ] Teste de acesso ao admin: `/admin/`

---

## 🎨 Deploy no Vercel (Frontend)

### Configuração Inicial
- [ ] Conta criada no Vercel
- [ ] Repositório conectado
- [ ] Projeto criado

### Configurações do Projeto
- [ ] Framework: Create React App
- [ ] Root Directory: `frontend`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `build`
- [ ] Install Command: `npm install`

### Variáveis de Ambiente
- [ ] `REACT_APP_API_URL` = URL do backend no Render

### Pós-Deploy
- [ ] Deploy concluído com sucesso
- [ ] URL do frontend anotada: `https://________________.vercel.app`
- [ ] Frontend acessível

---

## 🔄 Configuração Final

### Atualizar CORS no Backend
- [ ] Voltar ao Render
- [ ] Atualizar `CORS_ALLOWED_ORIGINS` com URL do Vercel
- [ ] Reiniciar serviço no Render

---

## 🧪 Testes Pós-Deploy

### Funcionalidades Básicas
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Navegação entre páginas funciona
- [ ] API responde corretamente

### Módulos
- [ ] Estoque - Produtos
- [ ] Estoque - Categorias
- [ ] Estoque - Movimentações
- [ ] Financeiro - Vendas
- [ ] Financeiro - Compras
- [ ] Financeiro - Clientes
- [ ] Financeiro - Contas a Pagar
- [ ] Financeiro - Contas a Receber
- [ ] Financeiro - Relatórios

### Mobile
- [ ] Layout responsivo funciona
- [ ] Menu lateral funciona
- [ ] Formulários funcionam
- [ ] Tabelas com scroll horizontal

---

## 🔐 Segurança

- [ ] `SECRET_KEY` forte e única
- [ ] `DEBUG=False` em produção
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS habilitado (automático no Render/Vercel)
- [ ] Cookies seguros configurados
- [ ] CORS configurado corretamente

---

## 📝 Documentação

- [ ] `DEPLOY.md` lido e seguido
- [ ] URLs anotadas
- [ ] Credenciais de acesso anotadas (em local seguro)

---

## 🎉 Pronto!

Após completar todos os itens, seu sistema estará em produção!

**URLs:**
- Backend: `https://________________.onrender.com`
- Frontend: `https://________________.vercel.app`

**Credenciais:**
- Usuário: `admin`
- Senha: `________________`

---

## 🆘 Problemas Comuns

### Backend não inicia
- Verificar logs no Render
- Confirmar variáveis de ambiente
- Verificar Start Command

### Frontend não conecta
- Verificar `REACT_APP_API_URL`
- Verificar CORS no backend
- Verificar console do navegador

### Erro 500
- Verificar logs
- Confirmar migrações executadas
- Verificar banco de dados

---

**Boa sorte! 🚀**

