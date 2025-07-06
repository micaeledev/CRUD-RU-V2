# Sistema CRUD - Gerenciamento de Usuários, Pedidos e Pagamentos

Sistema de gerenciamento com interface terminal (TUI) para operações CRUD em 3 tabelas relacionadas

## Funcionalidades

- **Gerenciar Usuários**: Cadastrar, listar, atualizar e deletar usuários
- **Gerenciar Pedidos**: Cadastrar, listar, atualizar e deletar pedidos
- **Gerenciar Pagamentos**: Cadastrar, listar, atualizar e deletar pagamentos

## Estrutura das Tabelas

```
Usuario (1) → Pedido (N) → Pagamento (N)
                ↓
             Cardapio (1)
                ↓
         Categoria_Usuario (1)
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   ```bash
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto:
   ```
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. Configure seu banco PostgreSQL/Supabase com as tabelas necessárias

## Uso

Execute o programa:
```bash
python main.py
```

Ou use os scripts batch (Windows):
```bash
setup.bat  # Para configurar o ambiente
run.bat    # Para executar o programa
```

## Tecnologias

- Python 3.x
- PostgreSQL/Supabase
- psycopg2 (conexão com banco)
- questionary (interface terminal)
- python-dotenv (variáveis de ambiente)

## Estrutura do Projeto

```
projeto bd/
├── main.py           # Arquivo principal
├── database.py       # Operações de banco de dados
├── tui.py           # Interface terminal
├── schema.sql       # Estrutura das tabelas
├── requirements.txt # Dependências
├── .env            # Configurações (não versionado)
├── setup.bat       # Script de configuração
└── run.bat         # Script de execução
```
