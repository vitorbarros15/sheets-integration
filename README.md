# 📊 Sheets Integration API

Uma API REST moderna desenvolvida em Python com FastAPI para integração com Google Sheets, permitindo leitura e escrita de dados de forma simples e eficiente.

## ✨ Funcionalidades

- 📖 **Leitura de dados** - Obter todos os registros de uma planilha
- ✍️ **Escrita de dados** - Adicionar novos registros à planilha
- 🚀 **API REST** - Interface RESTful com FastAPI
- 🔐 **Autenticação segura** - Integração segura com Google Sheets API
- 📝 **Validação de dados** - Validação automática com Pydantic
- 🐳 **Docker ready** - Containerização para deploy fácil

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Google Sheets API** - Integração oficial do Google
- **Pydantic** - Validação de dados
- **gspread** - Cliente Python para Google Sheets
- **uvicorn** - Servidor ASGI

## 📦 Instalação

### Pré-requisitos

- Python 3.8+
- Conta Google com acesso ao Google Sheets API
- Credenciais de service account do Google Cloud

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sheets-integration.git
cd sheets-integration
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
GOOGLE_CREDENTIALS_PATH=credentials/service-account.json
SHEET_NAME=Academia
DEBUG=True
```

### 5. Configure as credenciais do Google

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Habilite a Google Sheets API
4. Crie uma service account e baixe o arquivo JSON
5. Coloque o arquivo na pasta `credentials/`
6. Compartilhe sua planilha com o email da service account

## 🚀 Uso

### Executar a aplicação

```bash
# Desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

### Documentação interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 Endpoints da API

### GET /sheets/dados

Retorna todos os registros da planilha.

**Resposta:**
```json
[
  {
    "name": "João Silva",
    "serie": 3,
    "initial_weight": "80kg",
    "date": "2024-01-15"
  }
]
```

### POST /sheets/adicionar

Adiciona um novo registro à planilha.

**Body:**
```json
{
  "name": "Maria Santos",
  "serie": 5,
  "initial_weight": "65kg",
  "date": "2024-01-20"
}
```

**Resposta:**
```json
{
  "status": "Adicionado com sucesso!"
}
```

## 🐳 Docker

### Executar com Docker

```bash
# Build da imagem
docker build -t sheets-integration .

# Executar container
docker run -p 8000:8000 --env-file .env sheets-integration
```

### Docker Compose

```bash
docker-compose up -d
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app

# Executar testes específicos
pytest tests/test_sheets_service.py
```

## 🔧 Desenvolvimento

### Configurar ambiente de desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install

# Executar linting
flake8 app/
black app/
isort app/
```

### Estrutura do projeto

```
sheets-integration/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação principal
│   ├── config.py            # Configurações
│   ├── models/
│   │   ├── __init__.py
│   │   └── sheet_models.py  # Modelos Pydantic
│   ├── routes/
│   │   ├── __init__.py
│   │   └── sheets_routes.py # Rotas da API
│   └── services/
│       ├── __init__.py
│       └── sheets_service.py # Lógica de negócio
├── tests/                   # Testes
├── credentials/             # Credenciais (não versionado)
├── requirements.txt         # Dependências
├── requirements-dev.txt     # Dependências de desenvolvimento
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Docker Compose
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Documentação
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


## 👨‍💻 Autor

Desenvolvido com ❤️ por [Vitor Barros](https://github.com/vitorbarros15)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
