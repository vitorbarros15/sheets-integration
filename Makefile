.PHONY: help install install-dev test lint format clean run docker-build docker-run

# Cores para output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instala dependências de produção
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	pip install -r requirements.txt

install-dev: install ## Instala dependências de desenvolvimento
	@echo "$(YELLOW)Instalando dependências de desenvolvimento...$(NC)"
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Executa todos os testes
	@echo "$(YELLOW)Executando testes...$(NC)"
	pytest tests/ -v --cov=app --cov-report=term-missing

test-coverage: ## Executa testes com relatório de cobertura HTML
	@echo "$(YELLOW)Executando testes com cobertura...$(NC)"
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Relatório de cobertura salvo em htmlcov/index.html$(NC)"

lint: ## Executa linting (flake8, mypy)
	@echo "$(YELLOW)Executando linting...$(NC)"
	flake8 app/
	mypy app/ --ignore-missing-imports

format: ## Formata código (black, isort)
	@echo "$(YELLOW)Formatando código...$(NC)"
	black app/ tests/
	isort app/ tests/

format-check: ## Verifica formatação sem alterar arquivos
	@echo "$(YELLOW)Verificando formatação...$(NC)"
	black --check app/ tests/
	isort --check-only app/ tests/

quality: format lint test ## Executa verificações de qualidade completas

clean: ## Remove arquivos temporários
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf dist/
	rm -rf build/

run: ## Executa a aplicação em modo desenvolvimento
	@echo "$(YELLOW)Iniciando aplicação...$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Executa a aplicação em modo produção
	@echo "$(YELLOW)Iniciando aplicação (produção)...$(NC)"
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build: ## Constrói imagem Docker
	@echo "$(YELLOW)Construindo imagem Docker...$(NC)"
	docker build -t sheets-integration .

docker-run: ## Executa container Docker
	@echo "$(YELLOW)Executando container Docker...$(NC)"
	docker run -p 8000:8000 --env-file .env sheets-integration

docker-compose-up: ## Inicia serviços com docker-compose
	@echo "$(YELLOW)Iniciando serviços com docker-compose...$(NC)"
	docker-compose up -d

docker-compose-down: ## Para serviços do docker-compose
	@echo "$(YELLOW)Parando serviços do docker-compose...$(NC)"
	docker-compose down

logs: ## Mostra logs do container
	docker-compose logs -f sheets-integration

setup: install-dev ## Configuração inicial completa do projeto
	@echo "$(YELLOW)Configuração inicial...$(NC)"
	cp .env.example .env
	mkdir -p logs
	mkdir -p credentials
	@echo "$(GREEN)Projeto configurado! Não esqueça de:$(NC)"
	@echo "$(GREEN)1. Editar o arquivo .env com suas configurações$(NC)"
	@echo "$(GREEN)2. Adicionar suas credenciais do Google na pasta credentials/$(NC)"
	@echo "$(GREEN)3. Executar 'make run' para iniciar a aplicação$(NC)"

security: ## Verifica vulnerabilidades de segurança
	@echo "$(YELLOW)Verificando segurança...$(NC)"
	safety check -r requirements.txt
	bandit -r app/

deploy-check: quality security ## Verificações completas antes do deploy
	@echo "$(GREEN)✅ Todas as verificações passaram! Pronto para deploy.$(NC)" 