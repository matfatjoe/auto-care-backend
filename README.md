# **AutoCare – Backend** 🚗🛠️

**API para gerenciamento de serviços de estética automotiva.**

> 🚧 **Status do Projeto:** Em desenvolvimento – funcionalidades sendo implementadas com TDD, PostgreSQL e CI/CD via GitHub Actions.

---

## 📚 Índice

- [📌 Sobre o Projeto](#-sobre-o-projeto)
- [🔥 Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚀 Primeiros Passos para Desenvolvimento](#-primeiros-passos-para-desenvolvimento)
- [🔧 Comandos Úteis](#-comandos-úteis)
- [🧪 Qualidade e Padrões](#-qualidade-e-padrões)
- [📄 Licença](#-licença)

---

## 📌 Sobre o Projeto

Este repositório contém a API do **AutoCare**, um sistema voltado para profissionais de estética automotiva que desejam otimizar sua gestão operacional e financeira. Aqui são implementadas funcionalidades como cadastro de serviços, controle de estoque, gestão financeira e muito mais.

---

## 🔥 Funcionalidades

### 🚧 **Cadastro e Precificação de Serviços**
- Definir serviços com nome, descrição e preço por hora ou fixo  
- Cálculo automático do valor final com base no tempo gasto  
- Uso de produtos vinculado a cada serviço, com controle em ml e desconto no estoque  

### 🚧 **Gestão de Produtos e Acessórios**
- CRUD de produtos (com nome, descrição e preço da última compra)  
- Controle de estoque (opcional) e histórico de valores  
- Cálculo de custo dos serviços com base em insumos utilizados  

### 🔜 **Controle Financeiro**
- Exibição do faturamento por período  
- Comparativo entre serviços prestados  
- Cálculo de lucro líquido com base nos custos dos produtos utilizados  

### 🔜 **Gestão de Clientes e Agendamentos**
- Cadastro de clientes e histórico de atendimentos  
- Agendamento de serviços com lembretes e organização por horário  

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11  
- **Framework:** Django + Django REST Framework  
- **Banco de Dados:** PostgreSQL  
- **Infraestrutura:** Docker + Docker Compose  
- **CI/CD:** GitHub Actions para testes e validação

---

## 📂 Estrutura do Projeto

O repositório `auto-care-backend/` possui:

- Apps Django organizados por domínio funcional (ex: `services`, `products`, `clients`)
- Endpoints RESTful para consumo por frontend mobile e web
- Scripts e configuração Docker para ambiente de desenvolvimento
- Pipelines de integração contínua para validação automática

---

## 🚀 Primeiros Passos para Desenvolvimento

### 1. Clonar o projeto e instalar dependências
```bash
git clone https://github.com/seu-usuario/auto-care-backend.git
cd auto-care-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme seu ambiente local.

### 3. Subir containers com Docker
```bash
docker-compose up --build
```

---

## 🔧 Comandos Úteis

Criar um novo app Django:
```bash
docker-compose run django_core python manage.py startapp <nome_do_app>
```

Rodar migrações:
```bash
docker-compose run django_core python manage.py migrate
```

Criar superusuário:
```bash
docker-compose run django_core python manage.py createsuperuser
```

Rodar testes:
```bash
pytest
```

---

## 🧪 Qualidade e Padrões

- Testes automatizados com `pytest`, seguindo TDD  
- Cobertura mínima de 90% (`pytest --cov`)  
- Linting com `flake8`  
- Commits padronizados via [Conventional Commits](https://www.conventionalcommits.org/)  
- CI com GitHub Actions para garantir testes e lint antes de merge na `main`  

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

🌟 **API desenvolvida com foco em confiabilidade, performance e manutenção!**