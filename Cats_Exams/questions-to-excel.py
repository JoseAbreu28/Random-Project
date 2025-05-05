import os
import sys
import pandas as pd
from bs4 import BeautifulSoup

EXCEL_FICHEIRO = "questoes.xlsx"

def extrair_dados_html(caminho_html):
    with open(caminho_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    dados = []
    blocos = soup.find_all("div", class_="css-z7ydi3-SessionMCQuestion")

    for bloco in blocos:
        # Extrair ID
        id_texto = bloco.find_previous("div", string=lambda x: x and "ID:" in x)
        if id_texto:
            id_ = id_texto.get_text(strip=True).split("ID:")[-1].strip(")")
        else:
            id_ = str(hash(bloco.get_text()))  # fallback

        # Extrair pergunta
        pergunta_div = bloco.find("div", class_="tw-text-text tw-text-base")
        pergunta = pergunta_div.get_text(strip=True) if pergunta_div else "PERGUNTA_NAO_ENCONTRADA"

        # Procurar a resposta correta com as duas possíveis classes
        resposta_certa_div = bloco.find_next(lambda tag: (
            tag.name == "div" and
            "tw-border-success" in tag.get("class", []) or
            "tw-border-info" in tag.get("class", [])
        ))

        if resposta_certa_div:
            resposta_p = resposta_certa_div.find("p")
            resposta = resposta_p.get_text(strip=True) if resposta_p else resposta_certa_div.get_text(strip=True)
        else:
            resposta = "RESPOSTA_NAO_ENCONTRADA"

        dados.append({
            "ID": id_,
            "Pergunta": pergunta,
            "Resposta Certa": resposta
        })

    return dados

def carregar_excel_existente():
    if os.path.exists(EXCEL_FICHEIRO):
        return pd.read_excel(EXCEL_FICHEIRO, dtype={"ID": str})
    else:
        return pd.DataFrame(columns=["ID", "Pergunta", "Resposta Certa"])

def guardar_dados(dados_novos):
    df_existente = carregar_excel_existente()
    df_novo = pd.DataFrame(dados_novos)

    # Evitar duplicados com base no ID
    df_combinado = pd.concat([df_existente, df_novo], ignore_index=True)
    df_final = df_combinado.drop_duplicates(subset=["ID"])

    df_final.to_excel(EXCEL_FICHEIRO, index=False)
    print(f"{len(df_novo)} novas perguntas processadas. Total: {len(df_final)}")
    print(f"Excel atualizado: {EXCEL_FICHEIRO}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 nav_to_excel.py <ficheiro.html>")
        sys.exit(1)

    caminho_html = sys.argv[1]

    if not os.path.isfile(caminho_html):
        print(f"Ficheiro não encontrado: {caminho_html}")
        sys.exit(1)

    dados_extraidos = extrair_dados_html(caminho_html)
    guardar_dados(dados_extraidos)
