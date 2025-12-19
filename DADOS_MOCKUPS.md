# 📦 Dados Mockups Criados

## Resumo dos Dados

### ✅ Categorias (7)
1. **Camisetas** - Camisetas básicas e estampadas
2. **Calças** - Calças jeans, sociais e esportivas
3. **Vestidos** - Vestidos casuais e sociais
4. **Shorts** - Shorts e bermudas
5. **Blusas** - Blusas e blusões
6. **Saias** - Saias de diversos modelos
7. **Acessórios** - Cintos, bolsas e acessórios

### ✅ Produtos (47 produtos)

#### Camisetas (10 produtos)
- Camiseta Básica Branca (P, M, G)
- Camiseta Básica Preta (P, M, G)
- Camiseta Estampada Azul (M, G)
- Camiseta Polo Branca (M)
- Camiseta Polo Preta (M) ⚠️ *Estoque baixo*

#### Calças (9 produtos)
- Calça Jeans Skinny Azul (38, 40, 42)
- Calça Jeans Reta Preta (38, 40) ⚠️ *Estoque baixo*
- Calça Social Preta (38, 40)
- Calça Legging Preta (P, M)

#### Vestidos (8 produtos)
- Vestido Midi Floral (P, M, G)
- Vestido Longo Preto (P, M)
- Vestido Curto Rosa (P, M) ⚠️ *Estoque baixo*
- Vestido Casual Azul (M)

#### Shorts (5 produtos)
- Short Jeans Azul (38, 40)
- Short Esportivo Preto (M, G)
- Bermuda Cargo Bege (40)

#### Blusas (6 produtos)
- Blusa Manga Longa Branca (P, M)
- Blusa Manga Curta Rosa (M, G)
- Blusão Moletom Cinza (M, G)

#### Saias (5 produtos)
- Saia Midi Preta (P, M)
- Saia Curta Jeans (P, M)
- Saia Longa Estampada (M)

#### Acessórios (4 produtos)
- Cinto Couro Marrom (Único)
- Cinto Couro Preto (Único)
- Bolsa Tote Bege (Único)
- Bolsa Tote Preta (Único)

### ✅ Clientes (10 clientes)

1. **João Silva** - CPF: 123.456.789-00
   - Email: joao.silva@email.com
   - Telefone: (31) 99999-1111
   - Observação: Cliente frequente, prefere produtos básicos

2. **Maria Santos** - CPF: 987.654.321-00
   - Email: maria.santos@email.com
   - Telefone: (31) 99999-2222
   - Observação: Gosta de vestidos e acessórios

3. **Pedro Oliveira** - CPF: 456.789.123-00
   - Email: pedro.oliveira@email.com
   - Telefone: (31) 99999-3333
   - Observação: Compra principalmente calças e camisetas

4. **Ana Costa** - CPF: 789.123.456-00
   - Email: ana.costa@email.com
   - Telefone: (31) 99999-4444
   - Observação: Cliente VIP, sempre busca novidades

5. **Carlos Ferreira** - CPF: 321.654.987-00
   - Email: carlos.ferreira@email.com
   - Telefone: (31) 99999-5555
   - Observação: Prefere roupas esportivas

6. **Juliana Alves** - CPF: 654.321.789-00
   - Email: juliana.alves@email.com
   - Telefone: (31) 99999-6666
   - Observação: Interessada em moda casual

7. **Roberto Lima** - CPF: 147.258.369-00
   - Email: roberto.lima@email.com
   - Telefone: (31) 99999-7777
   - Observação: Cliente corporativo, compra roupas sociais

8. **Fernanda Rocha** - CPF: 258.369.147-00
   - Email: fernanda.rocha@email.com
   - Telefone: (31) 99999-8888
   - Observação: Gosta de cores vibrantes

9. **Lucas Martins** - CPF: 369.147.258-00
   - Email: lucas.martins@email.com
   - Telefone: (31) 99999-9999
   - Observação: Jovem, prefere estilo despojado

10. **Patrícia Gomes** - CPF: 159.357.486-00
    - Email: patricia.gomes@email.com
    - Telefone: (31) 99999-0000
    - Observação: Cliente fiel há 3 anos

## 📊 Estatísticas

- **Total de Categorias**: 7
- **Total de Produtos**: 47
- **Total de Clientes**: 10
- **Produtos com Estoque Baixo**: ~8 produtos (marcados com ⚠️)

## 🎯 Produtos com Estoque Baixo (para testar alertas)

Os seguintes produtos foram criados com estoque abaixo do mínimo para testar o sistema de alertas:

1. Camiseta Polo Preta - M (3 unidades, mínimo: 5)
2. Calça Jeans Reta Preta - 38 (2 unidades, mínimo: 5)
3. Calça Jeans Reta Preta - 40 (4 unidades, mínimo: 5)
4. Vestido Curto Rosa - P (1 unidade, mínimo: 3)
5. Vestido Curto Rosa - M (2 unidades, mínimo: 3)

## 🚀 Como Usar

### Criar todos os dados de uma vez:
```bash
cd backend
python manage.py shell -c "exec(open('create_all_mock_data.py').read())"
```

### Criar apenas categorias e produtos:
```bash
cd backend
python manage.py shell -c "exec(open('create_mock_data.py').read())"
```

### Criar apenas clientes:
```bash
cd backend
python manage.py shell -c "exec(open('create_mock_clientes.py').read())"
```

## 💡 Próximos Passos

Agora você pode:
1. ✅ Testar o sistema de alertas de estoque baixo
2. ✅ Criar vendas vinculadas aos clientes
3. ✅ Testar o histórico de compras por cliente
4. ✅ Visualizar os produtos no dashboard
5. ✅ Testar os relatórios financeiros

## 📝 Notas

- Todos os produtos têm preços de custo e venda configurados
- Alguns produtos foram criados com estoque baixo propositalmente para testar alertas
- Os clientes têm dados completos (CPF, email, telefone, endereço)
- Todos os dados são fictícios e servem apenas para testes


