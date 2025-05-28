import requests
import json
from collections import defaultdict

# Mapeie aqui os slugs base → Nome PT-BR que você quer suportar
TRADUCOES = {
    "route-1": "rota 1",
    "route-2": "rota 2",
    "route-3": "rota 3",
    "route-4": "rota 4",
    "route-5": "rota 5",
    "route-6": "rota 6",
    "route-7": "rota 7",
    "route-8": "rota 8",
    "route-9": "rota 9",
    "route-10": "rota 10",
    "route-11": "rota 11",
    "route-12": "rota 12",
    "route-13": "rota 13",
    "route-14": "rota 14",
    "route-15": "rota 15",
    "route-16": "rota 16",
    "route-17": "rota 17",
    "route-18": "rota 18",
    "nuvema-town": "vila nuvema",
    "accumula-town": "cidade acumula",
    "striaton-city": "cidade striaton",
    "flocessy-town": "vila flocessy",
    "castelia-city": "cidade castelia",
    "nimbasa-city": "cidade nimbasa",
    "driftveil-city": "cidade driftveil",
    "mistralton-city": "cidade mistralton",
    "icirrus-city": "cidade icirrus",
    "opelucid-city": "cidade opelucid",
    "lacunosa-town": "vila lacunosa",
    "undella-town": "cidade undella",
    "pinwheel-forest": "bosque pinwheel",
    "dreamyard": "dreamyard",
    "celestial-tower": "torre celestial",
    "chargestone-cave": "caverna elétrica",
    "mistralton-cave": "caverna mistralton",
    "desert-resort": "deserto"
}

def obter_todas_areas():
    resp = requests.get("https://pokeapi.co/api/v2/location-area?limit=10000")
    resp.raise_for_status()
    return resp.json()["results"]  # lista de dicts com 'name' e 'url'

def obter_encontros(area_url):
    r = requests.get(area_url)
    if r.status_code != 200:
        return []
    data = r.json()
    lista = []
    for enc in data.get("pokemon_encounters", []):
        nome_pkm = enc["pokemon"]["name"]
        for vd in enc.get("version_details", []):
            if vd["version"]["name"] not in ["black", "white"]:
                continue
            for det in vd.get("encounter_details", []):
                lista.append({
                    "pokemon": nome_pkm,
                    "metodo": det["method"]["name"],
                    "horario": det.get("time_of_day", "any"),
                    "chance": det.get("chance", 0)
                })
    return lista

def gerar_json_final():
    print("🔍 Buscando todas as áreas da PokéAPI...")
    all_areas = obter_todas_areas()

    banco = defaultdict(list)
    for slug_api, nome_pt in TRADUCOES.items():
        # filtra por substring
        matches = [a for a in all_areas if slug_api in a["name"]]
        if not matches:
            print(f"⚠️  Nenhuma área encontrada para '{slug_api}'")
            continue

        for area in matches:
            print(f"⬇️  Baixando {area['name']} → '{nome_pt}'")
            encontros = obter_encontros(area["url"])
            banco[nome_pt].extend(encontros)

    # remove duplicatas
    for nome_pt, lista in banco.items():
        vistos = set()
        dedup = []
        for e in lista:
            chave = (e["pokemon"], e["metodo"], e["horario"])
            if chave in vistos: continue
            vistos.add(chave)
            dedup.append(e)
        banco[nome_pt] = dedup

    # salva
    with open("pokemon_data.json", "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
    print("✅ 'pokemon_data.json' gerado com sucesso!")

if __name__ == "__main__":
    gerar_json_final()
