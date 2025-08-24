# 📋 Desafio Técnico - Desenvolvedor Python Conthabil

Sistema de automação para coleta, armazenamento e disponibilização de diários oficiais da prefeitura de Natal-RN. Desenvolvido como desafio técnico para vaga de Desenvolvedor Python.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Execução com Docker](#-execução-com-docker)
- [Execução Manual](#-execução-manual)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Configuração do Banco](#-configuração-do-banco)
- [Solução de Problemas](#-solução-de-problemas)
- [Adaptações Implementadas](#-adaptaçoes-implementadas)

## 🚀 Funcionalidades

- ✅ **Web Scraping** automatizado do site da prefeitura de Natal
- ✅ **Download e armazenamento** de PDFs dos diários oficiais
- ✅ **Sistema de upload** com URLs públicas
- ✅ **API REST** completa com documentação interativa
- ✅ **Banco de dados PostgreSQL** para metadados
- ✅ **Filtragem** por competência (mês/ano)
- ✅ **Dockerização** completa da aplicação
- ✅ **Interface de gerenciamento** do banco (PGAdmin)

## 🛠️ Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web moderno
- **Selenium** - Automação e scraping web
- **PostgreSQL** - Banco de dados relacional
- **Docker & Docker Compose** - Containerização
- **UVicorn** - Servidor ASGI de alta performance
- **WebDriver Manager** - Gerenciamento automático de drivers

## 📋 Pré-requisitos

### Para execução com Docker:
- Docker Engine 20.10+
- Docker Compose 2.0+

### Para execução manual:
- Python 3.8+
- PostgreSQL 12+
- Google Chrome
- ChromeDriver

## 🐳 Execução com Docker (Recomendado)

# Subir todos os serviços
docker-compose up --build

# Ou em segundo plano
docker-compose up -d --build

# Em outro terminal, execute o scraper
docker-compose exec api python -m app.services.scraper

4. Acesse os serviços
API Principal: http://localhost:8000
Documentação API: http://localhost:8000/docs
Servidor de Arquivos: http://localhost:8001/files/
PGAdmin: http://localhost:5050 (email: admin@admin.com, senha: admin)

# Clone o repositório
[git clone https://github.com/seu-usuario/diarios-oficiais-natal.git](https://github.com/DiegoCarvalho-dev/Desafio-Tecnico-CONTHABIL.git)
cd diarios-oficiais-natal

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

 ou
 
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# 💻 Execução Manual (Sem Docker)
# Clone o repositório
[git clone https://github.com/seu-usuario/diarios-oficiais-natal.git](https://github.com/DiegoCarvalho-dev/Desafio-Tecnico-CONTHABIL.git)
cd diarios-oficiais-natal

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

 ou
 
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o PostgreSQL
Certifique-se que o PostgreSQL está rodando com:

Host: localhost

Porta: 5432

Database: conthabil

Usuário: postgres

Senha: admin

# Execute os serviços em terminais separados
- Terminal 1 - API Principal:
uvicorn App.main:app --reload --host 0.0.0.0 --port 8000

- Terminal 2 - Servidor de Arquivos:
python App/local_server.py

- Terminal 3 - Scraper:
python -m App.services.scraper

# Acesse os serviços
API: http://localhost:8000

Arquivos: http://localhost:8001/files/

# 👨‍💻 Desenvolvimento
 Este projeto foi desenvolvido como parte do processo seletivo para Desenvolvedor Python na Conthabil, demonstrando habilidades em:

- Automação web com Selenium

- Desenvolvimento de APIs com FastAPI

- Gestão de banco de dados PostgreSQL

- Containerização com Docker

- Boas práticas de código e documentação
