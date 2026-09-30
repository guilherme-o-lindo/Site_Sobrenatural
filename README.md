# Site Sobrenatural

Projeto de um quiz sobre a série **Sobrenatural**, desenvolvido com **FastAPI**, **Jinja2**, **HTML/CSS** e **SQLite**.

## Estrutura

```text
Site Sobrenatural/
├── backend/
│   └── main.py
├── database/
│   └── rank.db
└── frontend/
    ├── assets/
    ├── css/
    ├── pages/
    └── index.html
```

## Requisitos

- Python 3.10 ou superior
- `pip`
- `cloudflared` — somente se quiser disponibilizar o servidor pela internet usando Cloudflare Tunnel

## 1. Criar o ambiente virtual

Abra o terminal na pasta `Site Sobrenatural`:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instalar as dependências

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

## 3. Iniciar o servidor

Entre na pasta `backend`:

```bash
cd backend
```

Depois execute:

```bash
uvicorn main:app --reload
```

O servidor ficará disponível em:

```text
http://127.0.0.1:8000
```

Abra esse endereço no navegador.

### Encerrar o servidor

No terminal onde o Uvicorn está executando:

```text
Ctrl + C
```

## 4. Iniciar o Cloudflare Tunnel

Com o servidor FastAPI já iniciado, abra **outro terminal**.

O comando para criar um Quick Tunnel é:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

O Cloudflare exibirá uma URL parecida com:

```text
https://alguma-coisa.trycloudflare.com
```

Acesse essa URL para abrir o site pela internet.

> O terminal do Uvicorn precisa continuar aberto enquanto o site estiver sendo executado.
> O terminal do `cloudflared` também precisa continuar aberto enquanto o Tunnel estiver ativo.

## Fluxo completo

São necessários dois terminais.

### Terminal 1 — FastAPI

```bash
cd "Site Sobrenatural/backend"
```

```bash
uvicorn main:app --reload
```

### Terminal 2 — Cloudflare Tunnel

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Depois, use a URL `https://*.trycloudflare.com` exibida pelo Cloudflare.

## Banco de dados

O projeto utiliza SQLite.

O banco fica em:

```text
database/rank.db
```

O `main.py` cria a tabela `ranking` automaticamente quando o servidor é iniciado, caso ela ainda não exista.

## Observação sobre o Cloudflare Tunnel

O comando usado acima cria um **Quick Tunnel**, indicado para testes e demonstrações.

A URL `trycloudflare.com` é temporária e pode mudar quando o Tunnel for encerrado e iniciado novamente.

Para um endereço permanente, é necessário configurar um **Cloudflare Tunnel nomeado** e vinculá-lo a um domínio.
