# Guia de Instalação - Sistema de Gestão de Estoque e Financeiro

Este guia fornece instruções passo a passo para instalar e configurar o sistema.

## Pré-requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- npm ou yarn
- PostgreSQL (opcional, SQLite é usado por padrão)

## Instalação do Backend

1. **Navegue até a pasta do backend:**
```bash
cd backend
```

2. **Crie um ambiente virtual:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o arquivo .env (opcional):**
```bash
# Copie o arquivo de exemplo
cp .env.example .env
# Edite o .env com suas configurações
```

5. **Execute as migrações:**
```bash
python manage.py migrate
```

6. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor:**
```bash
python manage.py runserver
```

O backend estará disponível em `http://localhost:8000`

## Instalação do Frontend

1. **Navegue até a pasta do frontend:**
```bash
cd frontend
```

2. **Instale as dependências:**
```bash
npm install
```

3. **Inicie o servidor de desenvolvimento:**
```bash
npm start
```

O frontend estará disponível em `http://localhost:3000`

## Primeiros Passos

1. Acesse o sistema em `http://localhost:3000`
2. Faça login com as credenciais do superusuário criado
3. Comece criando categorias de produtos
4. Adicione produtos ao estoque
5. Registre vendas e compras

## Estrutura do Projeto

```
.
├── backend/          # API Django
│   ├── estoque/      # App de gestão de estoque
│   ├── financeiro/   # App de gestão financeira
│   └── gestao/       # Configurações do projeto
├── frontend/         # App React
│   └── src/
│       ├── components/
│       ├── contexts/
│       └── services/
└── README.md
```

## Solução de Problemas

### Erro de CORS
Se encontrar erros de CORS, verifique se o `CORS_ALLOWED_ORIGINS` no `settings.py` inclui `http://localhost:3000`

### Erro de autenticação
Certifique-se de que o backend está rodando e que as credenciais estão corretas.

### Erro ao instalar dependências
- Backend: Verifique se está usando Python 3.8+
- Frontend: Tente limpar o cache: `npm cache clean --force`

## Próximos Passos

Consulte o README.md para mais informações sobre funcionalidades e uso do sistema.


