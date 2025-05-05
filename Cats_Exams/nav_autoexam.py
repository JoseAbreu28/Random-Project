import os
import sys
import pandas as pd
from bs4 import BeautifulSoup

EXCEL_FICHEIRO = "questoes.xlsx"

def carregar_excel():
    if os.path.exists(EXCEL_FICHEIRO):
        return pd.read_excel(EXCEL_FICHEIRO)
    else:
        print(f"Erro: Ficheiro {EXCEL_FICHEIRO} não encontrado.")
        sys.exit(1)

def extrair_perguntas_html(caminho_html):
    with open(caminho_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    perguntas = []
    blocos = soup.find_all("div", class_="css-z7ydi3-SessionMCQuestion")

    for bloco in blocos:
        pergunta_div = bloco.find("div", class_="tw-text-text tw-text-base")
        if pergunta_div:
            pergunta = pergunta_div.get_text(strip=True)
            perguntas.append(pergunta)
    return perguntas

def verificar_respostas(perguntas, df_excel):
    for idx, pergunta in enumerate(perguntas, start=1):
        match = df_excel[df_excel['Pergunta'].str.strip() == pergunta.strip()]
        print(f"Pergunta {idx} - {pergunta}")
        if not match.empty:
            resposta = match.iloc[0]["Resposta Certa"]
            print(f"Resposta - {resposta}")
        else:
            print("Resposta - Not Answer on the database")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 verificar_respostas.py <ficheiro.html>")
        sys.exit(1)

    caminho_html = sys.argv[1]

    if not os.path.isfile(caminho_html):
        print(f"Ficheiro não encontrado: {caminho_html}")
        sys.exit(1)

    df_excel = carregar_excel()
    perguntas = extrair_perguntas_html(caminho_html)
    verificar_respostas(perguntas, df_excel)
