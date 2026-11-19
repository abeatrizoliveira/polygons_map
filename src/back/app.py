import psycopg2
from flask import Flask, jsonify, render_template, request
from psycopg2.extras import Json

from . import db
from .classificacao import validar_tipo
from .geometria import ponto_em_poligono, validar_coordenada, validar_vertices

app = Flask(__name__, template_folder="..")


def erro(mensagem, status=400):
    return jsonify(erro=mensagem), status

# Um select das áreas -> pi{id,nome,tipo,coordenadas}(AREAS)
def carregar_areas(cur):
    cur.execute("SELECT id, nome, tipo, coordenadas FROM areas ORDER BY id")
    return cur.fetchall()

# trata erros do banco
@app.errorhandler(psycopg2.Error)
def erro_banco(e):
    app.logger.exception(e)
    return erro("Erro ao acessar o banco de dados. Confira DATABASE_URL e schema.sql.", 500)

# rota inicial
@app.get("/")
def index():
    return render_template("index.html")


# lista as areas (chama a função ali em cima que chama o banco)
@app.get("/api/areas")
def listar_areas():
    with db.cursor() as cur:
        return jsonify(carregar_areas(cur))


# cadastro de uma nova área
@app.post("/api/areas")
def criar_area():
    dados = request.get_json(silent=True) or {}
    nome = str(dados.get("nome", "")).strip()

    if not nome or len(nome) > 100:
        return erro("Informe um nome de até 100 caracteres.")
    
    try:
        tipo = validar_tipo(dados.get("tipo")) 
        vertices = validar_vertices(dados.get("coordenadas")) # valida as vértice
    except ValueError as e:
        return erro(str(e))
    with db.cursor() as cur: # se tudo deu certo, insere no banco
        cur.execute(
            "INSERT INTO areas (nome, tipo, coordenadas) VALUES (%s, %s, %s) RETURNING id", 
            (nome, tipo, Json(vertices)),
        )
        novo_id = cur.fetchone()["id"]
    return jsonify(id=novo_id), 201



# exclui uma área sigma{id=%d}(ALUNO)
@app.delete("/api/areas/<int:area_id>")
def excluir_area(area_id):
    with db.cursor() as cur:
        cur.execute("DELETE FROM areas WHERE id = %s", (area_id,))
        apagou = cur.rowcount > 0
    return ("", 204) if apagou else erro("Área não encontrada.", 404)


#  consulta "que tipo de área é este ponto?" pertencimento
@app.post("/api/consulta")
def consultar():
    dados = request.get_json(silent=True) or {}
    try:
        lat, lng = validar_coordenada(dados.get("lat"), dados.get("lng")) # valida coordenadas
    except ValueError as e:
        return erro(str(e))
    with db.cursor() as cur:
        areas = carregar_areas(cur) # consulta todas as áreas cadastradas no banco

    # varre todas as áreas -> se houver sobreposição, o ponto pertence a mais de uma 
    # Para cada área cadastrada -> verifica se o ponto informado ta dentro do polígono daquela área. Se estiver, adiciona a área em "contendo"
    contendo = [a for a in areas if ponto_em_poligono(lat, lng, a["coordenadas"])] # list comprehension -> o resultado pode ser representado assim: contendo = {a pertence A | P pertence a}
    
    tipos = sorted({a["tipo"] for a in contendo}) # pega o tipo das áreas encontradas que estão contidas, coloca em um conjunto para não haver repetição e ordena

    return jsonify(
    lat=lat,
    lng=lng,
    tipos=tipos,
    areas=[
        {"id": a["id"], "nome": a["nome"], "tipo": a["tipo"]}
        for a in contendo
    ],
)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
