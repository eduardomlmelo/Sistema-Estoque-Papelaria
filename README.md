# Sistema de Gerenciamento de Estoque - Papelaria

Um sistema simples e intuitivo para gerenciamento de estoque de loja de papelaria, desenvolvido em Python com interface gráfica (Tkinter).

## Funcionalidades

- ✅ **Cadastro de Produtos**: Adicionar novos produtos com nome, código, quantidade, preço, categoria e descrição
- ✅ **Busca e Filtro**: Busca em tempo real por nome ou código de produto
- ✅ **Atualização**: Editar informações de produtos existentes
- ✅ **Exclusão**: Remover produtos do estoque
- ✅ **Histórico**: Rastrear movimentações de entrada/saída de produtos
- ✅ **Relatórios**: Gerar relatórios em PDF do estoque

## Requisitos

- Python 3.13+
- pip ou uv (gerenciador de pacotes)

## Instalação

### 1. Clonar repositório
```bash
git clone <repository-url>
cd estoque_papelaria
```

### 2. Criar ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

## Uso

### Executar a aplicação
```bash
python src/app.py
```

A interface gráfica abrirá e você poderá:
1. **Novo**: Cadastrar um novo produto
2. **Editar**: Modificar dados de um produto selecionado
3. **Remover**: Deletar um produto (com confirmação)
4. **Buscar**: Filtrar produtos em tempo real
5. **Histórico**: Ver movimentações de um produto
6. **Gerar Relatório**: Exportar estoque para PDF

## Desenvolvimento

### Executar testes
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Apenas unit tests
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Teste específico
pytest tests/unit/test_validators.py::test_validate_product_name -v
```

### Estrutura do Projeto

```
estoque_papelaria/
├── src/
│   ├── models/           # Entidades de domínio
│   ├── database/         # Camada de persistência
│   ├── services/         # Lógica de negócio
│   ├── gui/              # Interface gráfica
│   ├── utils/            # Utilitários
│   └── app.py            # Entry point
├── tests/                # Testes automatizados
├── data/                 # Arquivos de dados (banco SQLite)
└── README.md
```

### Padrões de Código

- **Tipagem**: Type hints completos em todas as funções (Python 3.13)
- **Nomes**: snake_case para funções/variáveis, PascalCase para classes
- **Funções**: Pequenas e bem definidas (máx ~15 linhas)
- **Erros**: Tratamento explícito, sem silenciar exceções
- **Commits**: Conventional Commits (feat:, fix:, test:, chore:)

## Arquitetura

O sistema segue uma arquitetura em 3 camadas:

```
┌─ GUI (Tkinter) ─────────────────────┐
│  MainWindow, Dialogs                 │
└─────────────────────┬────────────────┘
                      ↓
┌─ Services ──────────────────────────┐
│  ProductService, ReportService       │
└─────────────────────┬────────────────┘
                      ↓
┌─ Database ──────────────────────────┐
│  Repository (CRUD), SQLite           │
└──────────────────────────────────────┘
```

### Benefícios

- **Testabilidade**: Lógica isolada de UI
- **Manutenibilidade**: Camadas bem definidas
- **Extensibilidade**: Fácil adicionar novas funcionalidades

## Contribuindo

1. Criar branch para a feature: `git checkout -b feat/nova-funcionalidade`
2. Fazer commits com mensagens descritivas
3. Enviar pull request

## Licença

MIT

## Screenshots

A aplicação possui interface intuitiva com:
- **Tabela de Produtos**: Lista todos os produtos com código, nome, quantidade, preço e categoria
- **Busca em Tempo Real**: Filtra produtos conforme você digita
- **Formulários**: Interface simples para adicionar e editar produtos
- **Histórico**: Visualiza todas as movimentações de cada produto
- **Relatórios**: Gera PDFs com listagem de estoque

## Estrutura do Banco de Dados

### Tabela: products
- id (INTEGER PRIMARY KEY)
- name (TEXT) - Nome do produto
- code (TEXT UNIQUE) - Código único do produto
- quantity (INTEGER) - Quantidade em estoque
- price (REAL) - Preço unitário
- category (TEXT) - Categoria
- description (TEXT) - Descrição
- created_at (TIMESTAMP) - Data de criação
- updated_at (TIMESTAMP) - Última atualização

### Tabela: stock_movements
- id (INTEGER PRIMARY KEY)
- product_id (INTEGER) - Referência ao produto
- quantity_change (INTEGER) - Quantidade adicionada/removida
- reason (TEXT) - Motivo (Entrada, Venda, Devolução, etc)
- timestamp (TIMESTAMP) - Data/hora da movimentação

## Exemplos de Uso

### Adicionar Produto
1. Clique em "Novo Produto"
2. Preencha os campos (todos obrigatórios)
3. Clique em "Salvar"
4. Produto aparecerá na tabela

### Buscar Produto
1. Digite no campo de busca
2. Tabela filtra automaticamente por nome ou código
3. Limpe o campo para ver todos novamente

### Editar Produto
1. Selecione o produto na tabela
2. Clique em "Editar"
3. Modifique os dados
4. Clique em "Salvar"
5. Alterações são gravadas no banco

### Remover Produto
1. Selecione o produto na tabela
2. Clique em "Remover"
3. Confirme a exclusão
4. Produto é deletado com todas suas movimentações

### Ver Histórico
1. Selecione um produto
2. Clique em "Histórico"
3. Veja todas as entradas/saídas com datas

### Gerar Relatório
1. Clique em "Relatório PDF"
2. Escolha filtros (todos os produtos ou por categoria)
3. Defina o caminho de destino
4. Clique em "Gerar"
5. PDF é criado com listagem formatada

## Tratamento de Erros

A aplicação valida todos os dados antes de salvar:
- ✓ Nome obrigatório (mín. 3 caracteres)
- ✓ Código único e obrigatório
- ✓ Quantidade não pode ser negativa
- ✓ Preço não pode ser negativo
- ✓ Categoria obrigatória
- ✓ Mensagens claras em caso de erro

## Performance

- **Busca**: Resultados instantâneos com índices SQLite
- **Banco de Dados**: SQLite com índices otimizados
- **Relatórios**: PDF gerado em segundos com reportlab

## Possíveis Melhorias Futuras

1. **Autenticação**: Sistema de login para múltiplos usuários
2. **Permissões**: Controle de acesso por papel (admin, vendedor, etc)
3. **Integração**: API REST para integrar com sistemas externos
4. **Gráficos**: Dashboard com gráficos de estoque e vendas
5. **Backup**: Exportar/importar banco de dados
6. **Notificações**: Alertas automáticos para estoque baixo
7. **Múltiplos Depósitos**: Controle de estoque em diferentes localidades
8. **Historico Detalhado**: Usuário que fez a movimentação, observações extras

## Contribuindo

Para contribuir com melhorias:
1. Crie uma branch: `git checkout -b feat/sua-feature`
2. Faça commits descritivos: `git commit -m "feat: descrição"`
3. Envie um pull request

## Licença

MIT - Veja LICENSE para detalhes

## Autor

Eduardo Matos - [eduardomatoslimam@gmail.com](mailto:eduardomatoslimam@gmail.com)

---

**Desenvolvido em Python 3.13 com Tkinter, SQLite e ReportLab**
