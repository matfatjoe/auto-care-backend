# **AutoCare** 🚗✨

**Gerencie seus serviços de estética automotiva de forma eficiente e profissional.**

## 📌 Sobre o Aplicativo
O **AutoCare** é um sistema desenvolvido para profissionais de estética automotiva que desejam otimizar a gestão financeira e operacional de seus serviços. Com ele, você pode cadastrar serviços, calcular preços automaticamente, gerenciar produtos e acessórios utilizados, acompanhar o faturamento e organizar sua agenda de clientes.

## 🔥 Funcionalidades Principais

### ❌ **Cadastro e Precificação de Serviços**  
- Definir serviços com nome, descrição e preço por hora ou fixo.  
- Permitir cálculo automático do valor final com base no tempo gasto.  

### ❌ **Gestão de Produtos e Acessórios**  
- CRUD para produtos frequentemente utilizados, incluindo nome e descrição.  
- Registro do valor pago na última compra de cada produto.  
- Controle de estoque (opcional) e acompanhamento de variação de preço.  
- Cadastro de acessórios comprados para calcular o custo total dos serviços.  

### ❌ **Controle Financeiro e Relatórios**  
- Exibir total faturado por período.  
- Comparar serviços mais lucrativos.  
- Calcular lucro líquido considerando custos de produtos e acessórios.  

### ❌ **Gestão de Clientes e Agendamentos**  
- Cadastro de clientes e histórico de serviços prestados.  
- Agenda para marcação de horários com lembretes e notificações.  

## 🛠️ Stack Tecnológica
- **Back-end:** Django (Python) + Django REST Framework  
- **Banco de Dados:** PostgreSQL  
- **Front-end:** React Native CLI (Mobile) + Next.js (Web)  
- **Infraestrutura:** Docker para conteinerização e Kubernetes para escalabilidade  
- **CI/CD:** Configuração automática para deploy contínuo  

## 📂 Estrutura do Projeto
O projeto será dividido em três repositórios principais:
- **`auto-care-backend/`** → Backend com Django + PostgreSQL  
- **`auto-care-frontend/`** → Frontend com React Native CLI e Next.js  
- **`auto-care-devops/`** → Infraestrutura com Docker, CI/CD e deploy automatizado  

## 🚀 Primeiros Passos para Desenvolvimento
1. **Configurar o Backend:**
   - Criar ambiente virtual e instalar Django
   - Configurar PostgreSQL
   - Criar modelos iniciais e endpoints REST
   - Implementar autenticação e autorização
   
2. **Configurar o Frontend:**
   - Criar estrutura do React Native CLI e Next.js
   - Definir navegação e componentes reutilizáveis
   - Implementar primeira tela de login
   
3. **Configurar a Infraestrutura:**
   - Criar Dockerfile e docker-compose
   - Configurar CI/CD para automação de testes e deploy
   - Criar ambiente de staging para testes

## 🔧 Comandos Úteis
### Backend (Django)
Rodar o servidor Django:
```bash
docker-compose up
```

Criar um novo app dentro do Django:
```bash
docker-compose exec django_core python manage.py startapp <nome_do_app>
```

Rodar migrações:
```bash
docker-compose exec django_core python manage.py migrate
```

Criar um superusuário para acessar o admin:
```bash
docker-compose exec django_core python manage.py createsuperuser
```

Instalar dependências:
```bash
docker-compose exec django_core pip install -r requirements.txt
```

Rodar testes Django:
```bash
docker-compose exec django_core python manage.py test
```

---

🌟 **Desenvolvido com foco na eficiência e praticidade!** 😊

