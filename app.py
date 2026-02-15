from flask import Flask, render_template, jsonify
import random
import json
import os


app = Flask(__name__)

# --- FUNÇÃO TÉCNICA PARA CARREGAR DADOS ---
def carregar_dados(arquivo):
    """Lê arquivos JSON na raiz do projeto com codificação UTF-8."""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo {arquivo} não encontrado!")
        return []

# --- CARREGAMENTO DOS DECKS (OCUPA APENAS 4 LINHAS AGORA!) ---
# Certifique-se de que os nomes dos arquivos .json sejam exatamente esses no seu PyCharm
meu_deck_80 = carregar_dados('deck_novo.json')
meu_deck = carregar_dados('rituais.json')
catalogo_geral = carregar_dados('catalogo_geral.json')
cartas_tarot = carregar_dados('tarot.json')

# União das listas para a Galeria
todos_rituais = meu_deck + catalogo_geral

# --- ROTAS DO SITE ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sorteador')
def sorteador():
    return render_template('index.html')

@app.route('/galeria')
def galeria():
    # A Galeria recebe a lista COMPLETA unificada
    return render_template('galeria.html', rituais=todos_rituais)

@app.route('/erro')
def erro():
    return render_template('erro.html')

@app.route('/sortear')
def sortear():
    # Atualmente sorteando do deck padrão.
    # Mude para 'meu_deck_80' se quiser testar o deck novo de Energia!
    ritual_sorteado = random.choice(meu_deck_80)
    return jsonify(ritual_sorteado)

@app.route('/tarot')
def tarot():
    """Renderiza a página visual do baralho de Tarot."""
    return render_template('tarot.html')

@app.route('/sortear_tarot')
def sortear_tarot():
    """Retorna uma carta aleatória do deck de Tarot."""
    if not cartas_tarot:
        return jsonify({"erro": "Deck de tarot vazio ou não encontrado"}), 404
    return jsonify(random.choice(cartas_tarot))

if __name__ == '__main__':
    # Configuração para rodar localmente e ser compatível com o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)