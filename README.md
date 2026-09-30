# 🕵️ Site Sobrenatural

Quiz interativo inspirado na série **Sobrenatural**, desenvolvido como um projeto de estudo para praticar **Python, FastAPI, Jinja2, HTML, CSS e SQLite**.

O usuário responde 10 perguntas sobre a série, recebe sua pontuação e pode conferir suas respostas, além de visualizar o **ranking de participantes**.

---

## ✨ Funcionalidades

* 🎬 Página inicial temática
* 📝 Quiz com 10 perguntas
* 👤 Identificação do usuário
* 🧮 Cálculo automático da pontuação
* 📊 Página de resultado
* ✅ Comparação entre respostas e gabarito
* 🏆 Ranking de participantes
* 💾 Armazenamento das tentativas em SQLite
* 🌐 Possibilidade de disponibilizar o site pela internet usando Cloudflare Tunnel

---

## 🛠️ Tecnologias

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
</p>

---

## 📂 Estrutura

```text
Site Sobrenatural/
│
├── backend/
│   └── main.py
│
├── database/
│   └── rank.db
│
├── frontend/
│   ├── assets/
│   │   ├── icons/
│   │   └── imgs/
│   │
│   ├── css/
│   │   ├── quiz.css
│   │   ├── ranking.css
│   │   ├── resultado.css
│   │   └── style.css
│   │
│   ├── pages/
│   │   ├── quiz.html
│   │   ├── ranking.html
│   │   └── resultado.html
│   │
│   └── index.html
│
└── README.md
```

### Backend

O backend foi desenvolvido com **FastAPI** e é responsável por:

* Servir as páginas através do Jinja2
* Receber as respostas do quiz
* Calcular a pontuação
* Salvar as tentativas no SQLite
* Consultar o ranking
* Enviar os dados para as páginas de resultado

### Frontend

O frontend utiliza **HTML, CSS e Jinja2**.

As páginas principais são:

| Página           | Função                    |
| ---------------- | ------------------------- |
| `index.html`     | Página inicial            |
| `quiz.html`      | Questionário              |
| `resultado.html` | Resultado da tentativa    |
| `ranking.html`   | Ranking dos participantes |

---

## 🔄 Funcionamento

O fluxo principal do projeto funciona da seguinte maneira:

```text
Página inicial
      │
      ▼
Informar nome
      │
      ▼
      Quiz
      │
      ▼
Enviar respostas
      │
      ▼
FastAPI calcula pontuação
      │
      ▼
SQLite salva tentativa
      │
      ▼
Página de resultado
      │
      ▼
Ranking
```

Cada tentativa recebe um identificador próprio no banco de dados, permitindo recuperar posteriormente o resultado correspondente.

---

## 🌐 Rotas

O backend possui as seguintes rotas principais:

| Método | Rota                  | Função                        |
| ------ | --------------------- | ----------------------------- |
| `GET`  | `/`                   | Página inicial                |
| `POST` | `/api/iniciar-quiz`   | Inicia o quiz                 |
| `GET`  | `/quiz`               | Exibe o quiz                  |
| `POST` | `/api/responder-quiz` | Processa e salva as respostas |
| `GET`  | `/resultado`          | Exibe o resultado             |
| `GET`  | `/ranking`            | Exibe o ranking               |

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** para armazenar as tentativas realizadas no quiz.

O banco está localizado em:

```text
database/rank.db
```

A tabela utilizada é:

```text
ranking
```

Cada registro armazena:

* ID da tentativa
* Nome do usuário
* Pontuação
* Resposta de cada uma das 10 questões

A tabela é criada automaticamente pelo backend caso ainda não exista.

---

# 🚀 Como executar

## Requisitos

Antes de iniciar, tenha instalado:

* [Python](https://www.python.org/) 3.10 ou superior
* `pip`

Opcionalmente:

* [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) para disponibilizar o projeto pela internet

---

## 1. Clonar o repositório

```bash
git clone https://github.com/guilherme-o-lindo/Site-Sobrenatural.git
```

Entre na pasta:

```bash
cd Site-Sobrenatural
```

---

## 2. Criar o ambiente virtual

### Windows

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

---

## 3. Instalar as dependências

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

---

## 4. Iniciar o servidor

Entre na pasta `backend`:

```bash
cd backend
```

Inicie o FastAPI:

```bash
uvicorn main:app --reload
```

O servidor será iniciado em:

```text
http://127.0.0.1:8000
```

Abra o endereço no navegador.

---

## 🛑 Encerrar o servidor

No terminal onde o Uvicorn está executando:

```text
Ctrl + C
```

---

# ☁️ Cloudflare Tunnel

O projeto pode ser disponibilizado temporariamente pela internet utilizando um **Cloudflare Quick Tunnel**.

> O Cloudflare Tunnel não é necessário para executar o projeto localmente.

## 1. Inicie o FastAPI

Em um terminal:

```bash
cd backend
uvicorn main:app --reload
```

Mantenha esse terminal aberto.

## 2. Abra outro terminal

Na pasta do projeto, execute:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

O Cloudflare exibirá uma URL semelhante a:

```text
https://alguma-coisa.trycloudflare.com
```

Essa será a URL pública do projeto.

### Fluxo

```text
Terminal 1
    │
    └── FastAPI
        http://127.0.0.1:8000

Terminal 2
    │
    └── Cloudflare Tunnel
        https://alguma-coisa.trycloudflare.com
```

Os dois processos precisam continuar executando enquanto o site estiver sendo acessado.

### ⚠️ Sobre o Quick Tunnel

O Quick Tunnel é destinado principalmente a **testes, estudos e demonstrações**.

A URL `trycloudflare.com` é temporária e pode mudar quando o Tunnel for encerrado e iniciado novamente.

Para utilizar um endereço permanente, é necessário configurar um **Cloudflare Tunnel nomeado** e, normalmente, vinculá-lo a um domínio.

---

## 📚 O que estou praticando

Este projeto foi desenvolvido principalmente para colocar em prática conceitos de:

### Python

* Variáveis
* Funções
* Estruturas condicionais
* Dicionários
* Loops
* Manipulação de dados
* Módulos
* `sqlite3`
* Organização de código

### FastAPI

* Criação de aplicações
* Rotas `GET` e `POST`
* Formulários
* `Request`
* Redirecionamentos
* Arquivos estáticos
* Jinja2 Templates

### Banco de dados

* SQLite
* Conexão com banco
* Criação de tabelas
* `INSERT`
* `SELECT`
* Ordenação de resultados
* Recuperação de registros

### Frontend

* HTML semântico
* CSS
* Formulários
* Templates Jinja2
* Organização de páginas e estilos

---

## 🎯 Objetivo do projeto

O objetivo deste projeto é servir como uma aplicação prática para consolidar meus estudos em **Python e desenvolvimento web**, indo além de exercícios isolados.

A partir dele, estou praticando a comunicação entre:

```text
Frontend
   ↕
FastAPI
   ↕
SQLite
```

O projeto também serve como base para experimentar posteriormente novas funcionalidades e formas de organização de aplicações web.

---

## 📌 Status

**Em desenvolvimento / estudos**

Novas funcionalidades e melhorias podem ser adicionadas conforme os estudos avançarem.

---

<p align="center">
  🕵️ Python • FastAPI • Jinja2 • SQLite • HTML • CSS
</p>
