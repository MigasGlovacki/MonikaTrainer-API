from flask import Flask, request, jsonify
import json
import os
from familias_evolutivas import familias_evolutivas

app = Flask(__name__)

# Carrega banco de Pokémon por rota
def load_pokemon_data():
    with open("pokemon_data.json", "r", encoding="utf-8") as f:
        return json.load(f)
dados_por_rota = load_pokemon_data()

# Carrega capturados
def load_capturados():
    path = "capturados.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()
capturados = load_capturados()

# Carrega favor
favor_path = "favor.json"
def load_favor():
    if os.path.exists(favor_path):
        with open(favor_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"disponiveis": 0}
favor = load_favor()

# Carrega itens (vara de pescar)
itens_path = "itens.json"
def load_itens():
    if os.path.exists(itens_path):
        with open(itens_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"has_rod": False, "rod_type": None}
itens = load_itens()

# Carrega dicionário de tradução de nomes de rota
with open("tradutores.json", "r", encoding="utf-8") as f:
    nomes_traduzidos = json.load(f)

# Verifica se Pokémon ou sua evolução já foi capturado
def ja_capturado_ou_evolucao(pokemon):
    for capturado in capturados:
        if pokemon in familias_evolutivas.get(capturado, [capturado]):
            return True
    return False

# Endpoint: retorna Pokémon disponíveis na rota
@app.route("/get_pokemon_da_rota", methods=["POST"])
def get_pokemon_da_rota():
    rota = request.json.get("rota", "").lower().strip()
    rota = nomes_traduzidos.get(rota, rota)

    if rota not in dados_por_rota:
        return jsonify({"erro": f"Rota '{rota}' não encontrada."}), 404

    candidatos = []
    for p in dados_por_rota[rota]:
        met = p.get("metodo", "walk")
        # Se não tem vara, só permite encontros a pé (walk)
        if not itens.get("has_rod", False) and met != "walk":
            continue
        if ja_capturado_ou_evolucao(p["pokemon"]):
            continue
        candidatos.append(p)

    if not candidatos:
        return jsonify({"mensagem": "Todos os Pokémon dessa rota já foram capturados. Use um 'Monika’s Favor' 😉"})

    escolhido = candidatos[0]
    return jsonify({
        "escolhido": escolhido,
        "comentario": f"{escolhido['pokemon']} parece uma boa escolha~ nada repetido por aqui!"
    })

# Endpoint: registra Pokémon capturado
@app.route("/registrar_captura", methods=["POST"])
def registrar_captura():
    nome = request.json.get("pokemon", "").lower()
    if nome:
        capturados.add(nome)
        with open("capturados.json", "w", encoding="utf-8") as f:
            json.dump(sorted(list(capturados)), f, indent=2)
        return jsonify({"ok": True, "capturados": list(capturados)})
    return jsonify({"erro": "Nome do Pokémon ausente."}), 400

# Endpoint: ganha 1 favor
@app.route("/ganhar_favor", methods=["POST"])
def ganhar_favor():
    if favor["disponiveis"] < 2:
        favor["disponiveis"] += 1
        with open(favor_path, "w", encoding="utf-8") as f:
            json.dump(favor, f, indent=2)
    return jsonify({"ok": True, "favor_restante": favor["disponiveis"]})

# Endpoint: usa 1 favor
@app.route("/usar_favor", methods=["POST"])
def usar_favor():
    if favor["disponiveis"] > 0:
        favor["disponiveis"] -= 1
        with open(favor_path, "w", encoding="utf-8") as f:
            json.dump(favor, f, indent=2)
        return jsonify({"ok": True, "favor_restante": favor["disponiveis"]})
    return jsonify({"erro": "Você não tem nenhum Monika’s Favor!"}), 403

# Endpoint: consulta favor
@app.route("/ver_favor", methods=["GET"])
def ver_favor():
    return jsonify(favor)

# Endpoint: registra item (vara de pescar)
@app.route("/registrar_item", methods=["POST"])
def registrar_item():
    nome_item = request.json.get("item")
    if nome_item in ["old-rod", "good-rod", "super-rod"]:
        itens["has_rod"] = True
        itens["rod_type"] = nome_item
        with open(itens_path, "w", encoding="utf-8") as f:
            json.dump(itens, f, indent=2)
        return jsonify({"ok": True, "itens": itens})
    return jsonify({"erro": "Item desconhecido"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
