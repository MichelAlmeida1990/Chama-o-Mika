# Sistema de Gestão de Estoque e Financeiro para Roupas

Sistema completo de gestão de estoque e financeiro desenvolvido com Django (backend) e React (frontend).

## 🚀 Tecnologias

- **Backend**: Django + Django REST Framework
- **Frontend**: React + Bootstrap + Axios
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Outras**: Pandas (relatórios), Chart.js (gráficos)

## 📋 Funcionalidades

### Gestão de Estoque
- Cadastro de produtos (roupas) com atributos (tamanho, cor, modelo)
- Controle de entradas/saídas
- Alertas de estoque baixo
- Relatórios de inventário

### Gestão Financeira
- Registro de vendas/compras
- Contas a pagar/receber
- Relatórios financeiros (balanço, fluxo de caixa)
- Integração automática com estoque

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Node.js 14+
- PostgreSQL (opcional, SQLite para desenvolvimento)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## 📁 Estrutura do Projeto

```
.
├── backend/          # API Django
│   ├── gestao/       # App principal
│   ├── manage.py
│   └── requirements.txt
├── frontend/         # App React
│   ├── src/
│   └── package.json
└── README.md
```

## 🔐 Primeiro Acesso

1. Após criar o superusuário com `python manage.py createsuperuser`
2. Acesse `http://localhost:3000`
3. Faça login com as credenciais criadas
4. Comece criando categorias e produtos

## 📚 Documentação Adicional

Consulte o arquivo `INSTALACAO.md` para um guia detalhado de instalação.

## 📝 Licença

Este projeto é open-source e gratuito.

