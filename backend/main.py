from pathlib import Path
import sqlite3
import json

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import urlencode


app = FastAPI()


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"

DATABASE = BASE_DIR / "database" / "rank.db"


# ============================================================
# JINJA2
# ============================================================

templates = Jinja2Templates(
    directory=FRONTEND_DIR
)


# ============================================================
# ARQUIVOS ESTÁTICOS
# ============================================================

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)


# ============================================================
# BANCO DE DADOS
# ============================================================

def criar_banco():

    conexao = sqlite3.connect(DATABASE)

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            pontos INTEGER NOT NULL,

            q1 TEXT NOT NULL,
            q2 TEXT NOT NULL,
            q3 TEXT NOT NULL,
            q4 TEXT NOT NULL,
            q5 TEXT NOT NULL,
            q6 TEXT NOT NULL,
            q7 TEXT NOT NULL,
            q8 TEXT NOT NULL,
            q9 TEXT NOT NULL,
            q10 TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


criar_banco()


# ============================================================
# CONSULTAR RANKING
# ============================================================

def obter_ranking():

    conexao = sqlite3.connect(DATABASE)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT usuario, pontos
        FROM ranking
        ORDER BY pontos DESC
    """)

    ranking = cursor.fetchall()

    conexao.close()

    return ranking


# ============================================================
# INDEX
# ============================================================

@app.get("/")
def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ============================================================
# INICIAR QUIZ
# ============================================================

@app.post("/api/iniciar-quiz")
def iniciar_quiz(
    usuario: str = Form(...)
):

    print(f"Usuário: {usuario}")

    params = urlencode({"usuario": usuario})

    return RedirectResponse(
        url=f"/quiz?{params}",
        status_code=303
    )


# ============================================================
# QUIZ
# ============================================================

@app.get("/quiz")
def quiz(
    request: Request,
    usuario: str
):

    return templates.TemplateResponse(
        request=request,
        name="pages/quiz.html",
        context={
            "usuario": usuario
        }
    )


# ============================================================
# RESPONDER QUIZ
# ============================================================

@app.post("/api/responder-quiz")
def responder_quiz(
    usuario: str = Form(...),
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...),
    q6: str = Form(...),
    q7: str = Form(...),
    q8: str = Form(...),
    q9: str = Form(...),
    q10: str = Form(...),
):

    # -------------------------
    # GABARITO
    # -------------------------

    gabarito = {
        "q1": "michael",
        "q2": "impala",
        "q3": "lazarus",
        "q4": "meg",
        "q5": "miracle",
        "q6": "william",
        "q7": "campbell",
        "q8": "blade",
        "q9": "fergus",
        "q10": "nick"
    }


    # -------------------------
    # RESPOSTAS
    # -------------------------

    respostas = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10
    }


    # -------------------------
    # CALCULAR PONTOS
    # -------------------------

    pontos = 0

    for questao, resposta_certa in gabarito.items():

        if respostas[questao] == resposta_certa:
            pontos += 1


    print(f"Usuário: {usuario}")
    print(f"Pontuação: {pontos}/10")


    # -------------------------
    # SALVAR NO BANCO
    # -------------------------

    conexao = sqlite3.connect(DATABASE)

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO ranking (
            usuario,
            pontos,
            q1,
            q2,
            q3,
            q4,
            q5,
            q6,
            q7,
            q8,
            q9,
            q10
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario,
        pontos,
        q1,
        q2,
        q3,
        q4,
        q5,
        q6,
        q7,
        q8,
        q9,
        q10
    ))

    conexao.commit()

    # ID da tentativa que acabou de ser criada
    resultado_id = cursor.lastrowid

    conexao.close()


    # -------------------------
    # IR PARA RESULTADO
    # -------------------------

    return RedirectResponse(
        url=f"/resultado?id={resultado_id}",
        status_code=303
    )


# ============================================================
# RESULTADO
# ============================================================

@app.get("/resultado")
def resultado(
    request: Request,
    id: int
):

    conexao = sqlite3.connect(DATABASE)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            usuario,
            pontos,
            q1,
            q2,
            q3,
            q4,
            q5,
            q6,
            q7,
            q8,
            q9,
            q10
        FROM ranking
        WHERE id = ?
    """, (id,))

    resultado = cursor.fetchone()

    conexao.close()


    # -------------------------
    # RESULTADO NÃO ENCONTRADO
    # -------------------------

    if resultado is None:
        return {"erro": "Resultado não encontrado."}


    # -------------------------
    # ORGANIZAR DADOS
    # -------------------------

    usuario = resultado[0]
    pontos = resultado[1]

    respostas = {
        "q1": resultado[2],
        "q2": resultado[3],
        "q3": resultado[4],
        "q4": resultado[5],
        "q5": resultado[6],
        "q6": resultado[7],
        "q7": resultado[8],
        "q8": resultado[9],
        "q9": resultado[10],
        "q10": resultado[11]
    }


    # -------------------------
    # GABARITO
    # -------------------------

    gabarito = {
        "q1": "michael",
        "q2": "impala",
        "q3": "lazarus",
        "q4": "meg",
        "q5": "miracle",
        "q6": "william",
        "q7": "campbell",
        "q8": "blade",
        "q9": "fergus",
        "q10": "nick"
    }


    # -------------------------
    # VERIFICAR RESPOSTAS
    # -------------------------

    respostas_resultado = {}

    for questao in gabarito:

        respostas_resultado[questao] = {
            "resposta_usuario": respostas[questao],
            "resposta_certa": gabarito[questao],
            "correta": respostas[questao] == gabarito[questao]
        }


    # -------------------------
    # RANKING
    # -------------------------

    ranking = obter_ranking()


    # -------------------------
    # MENSAGEM
    # -------------------------

    if pontos <= 2:
        mensagem = f"Calma, {usuario}... talvez seja hora de assistir Sobrenatural de novo. 👀"

    elif pontos <= 4:
        mensagem = f"Você conhece Sobrenatural, {usuario}, mas ainda está longe de ser um Hunter."

    elif pontos <= 6:
        mensagem = f"Não está mal, {usuario}! Você já conhece bastante do universo de Sobrenatural."

    elif pontos <= 8:
        mensagem = f"Muito bom, {usuario}! Você realmente conhece Sobrenatural."

    elif pontos == 9:
        mensagem = f"Impressionante, {usuario}! Você está praticamente no nível de um Hunter experiente."

    else:
        mensagem = f"Perfeito, {usuario}! Você é oficialmente um verdadeiro fã de Sobrenatural. 🔥"


    # -------------------------
    # TEMPLATE
    # -------------------------

    return templates.TemplateResponse(
        request=request,
        name="pages/resultado.html",
        context={
            "usuario": usuario,
            "pontos": pontos,
            "mensagem": mensagem,
            "respostas": respostas_resultado,
            "ranking": ranking
        }
    )


# ============================================================
# RANKING
# ============================================================

@app.get("/ranking")
def ranking(request: Request):

    ranking = obter_ranking()

    return templates.TemplateResponse(
        request=request,
        name="pages/ranking.html",
        context={
            "ranking": ranking
        }
    )