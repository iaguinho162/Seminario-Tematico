# 🛒 Sistema de Marketplace com Microsserviços

Este projeto é um **Marketplace desenvolvido utilizando arquitetura de microsserviços**, onde os serviços são independentes, se comunicam entre si e utilizam mensageria assíncrona. Além disso, há integração com a API do **Mercado Pago** para processamento de pagamentos.

## 🔗 Tecnologias Utilizadas

- Python (FastAPI)
- Docker & Docker Compose
- RabbitMQ (mensageria)
- API Mercado Pago (pagamentos externos)
- Swagger / OpenAPI (documentação das APIs)
- Banco de dados (Dicionários em memória, mas adaptável para bancos relacionais)

---

## ⚙️ Arquitetura do Sistema

- **Serviço de Usuários:** Gerenciamento de usuários.
- **Serviço de Produtos:** Cadastro e gerenciamento de produtos.
- **Serviço de Pedidos:** Criação de pedidos e integração com Mercado Pago.
- **RabbitMQ:** Comunicação assíncrona para eventos (ex.: status de pagamento).
- **Mercado Pago:** Processamento de pagamentos (PIX, boleto, cartão).

---

## 🚀 Como Executar Localmente

### 🔥 Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) instalado


🐳 Execute com Docker Compose

docker-compose up --build

🌐 Acessando as APIs
Serviço	URL	Documentação Swagger
Usuários	http://localhost:8001	
Produtos	http://localhost:8002	
Pedidos	http://localhost:8003	
RabbitMQ	http://localhost:15672 (login: guest/guest)	

💳 Pagamento com Mercado Pago
O serviço de pedidos está integrado à API Mercado Pago Sandbox.

Permite pagamentos por PIX, boleto ou cartão de crédito.

No momento do pagamento, o cliente escolhe a forma de pagamento.


🔗 Endpoints Principais
🔸 Serviço de Usuários
POST /usuarios/ - Criar usuário

GET /usuarios/{id} - Buscar usuário

🔸 Serviço de Produtos
POST /produtos/ - Criar produto

GET /produtos/{id} - Buscar produto

🔸 Serviço de Pedidos
POST /pedidos/ - Criar pedido

GET /pedidos/ - Listar pedidos

GET /formas-pagamento/ - Consultar formas de pagamento disponíveis

POST /pagamento/{pedido_id}?metodo_pagamento=pix - Realizar pagamento


📦 Estrutura do Projeto
├── users/
├── products/
├── orders/
├── docker-compose.yml
├── README.md
Cada pasta contém o respectivo microsserviço com:

main.py

models.py

routes.py

Dockerfile

requirements.txt

🐇 RabbitMQ
A fila de mensageria é usada para enviar notificações de atualização de status de pedidos após confirmação do pagamento.

Acesse a interface do RabbitMQ:
👉 http://localhost:15672
Login: guest | Senha: guest

🛠️ Possíveis Melhorias Futuras

Frontend web
Observabilidade com Prometheus + Grafana


OBSERVAÇÕES: INSERIR NO TOKEN DO MERCADO PAGO E COLOCAR NA VARIAVEL: " ACCESS_TOKEN = "" "

### 📥 Clone o repositório

```bash
git clone https://github.com/seu-usuario/marketplace-microsservicos.git
cd marketplace-microsservicos
