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

## Autor

Eduardo Matos - [eduardomatoslimam@gmail.com](mailto:eduardomatoslimam@gmail.com)
