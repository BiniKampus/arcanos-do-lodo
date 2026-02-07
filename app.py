from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Aqui é o seu estoque de cartas.
# "img" precisa ser o nome exato da imagem que está na pasta 'static'
meu_deck = [
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Cicatrização", "img": "cicatrizacao.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Você acelera o tempo ao redor das feridas do alvo, que cicatrizam instantaneamente. O alvo recupera 3d8+3 PV, mas envelhece 1 ano automaticamente.. (Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Decadência", "img": "decadencia.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Espirais de trevas envolvem sua mão e definham o alvo, que sofre 2d8+2 pontos de dano de Morte. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Deflagração de Energia", "img": "deflagracao-de-energia.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4, "desc":"Você acumula uma quantidade imensa de Energia, então a libera em uma explosão intensa, como uma estrela em plena terra. Todos na área sofrem 3d10 x 10 pontos de dano de Energia (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Desacelerar Impacto", "img": "desacelerar-impacto.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2, "desc":"O alvo cai lentamente. A velocidade da queda é reduzida para 18m por rodada — o suficiente para não causar dano. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Descarnar", "img": "descarnar.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2, "desc":"A pele do alvo é dilacerada, abrindo cortes profundos. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Eco Espiral", "img": "eco-espiral.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2, "desc":"Repete o dano que o alvo sofreu ao longo das rodadas concentrando. (Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Eletrocussão", "img": "eletrocussao.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Corrente voltaica eletrocuta o alvo.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Espirais da Perdição", "img": "espirais-da-perdicao.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Inimigos sofrem penalidade em ataque.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Ferver Sangue", "img": "ferver-sangue.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3, "desc":"Faz o sangue do alvo entrar em ebulição, causando dano e deixando-o fraco.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Hemofagia", "img": "hemofagia.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2, "desc":"Absorve o sangue do alvo, causando dano e recuperando seus pontos de vida.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Invadir Mente", "img": "invadir-mente.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2, "desc":"Gera uma rajada mental ou se conecta telepaticamente.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Mergulho Mental", "img": "mergulho-mental.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3, "desc":"Se infiltra na mente do alvo para vasculhar seus pensamentos.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Perturbação", "img": "perturbacao.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1, "desc":"Força o alvo a obedecer a uma ordem.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Purgatório", "img": "purgatorio.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3, "desc":"Área de sangue deixa alvos vulneráveis a dano e causa dor a quem tentar sair.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Salto Fantasma", "img": "salto-fantasma.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3, "desc":"Teletransporta você e outros seres para um ponto dentro do alcance.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Tela de Ruído", "img": "tela-de-ruido.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2, "desc":"Cria uma película protetora que absorve dano.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Tentáculos de Lodo", "img": "tentaculos-de-lodo.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3, "desc":"Tentáculos pretos atacam e agarram seres na área.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Zerar Entropia", "img": "zerar-entropia.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3, "desc":"O alvo fica lento ou paralisado.(Para melhor descrição abra o livro de regras na página 143)"},
]

catalogo_geral = [
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Tecnologia", "img": "amaldicoar-tecnologia.png", "circulo": "1ºCírculo", "elemento": "Energia", "pe": 1,
     "desc": "Aprimora um item.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Arma Atroz", "img": "arma-atroz.png", "circulo": "1ºCírculo", "elemento": "Sangue", "pe": 1,
     "desc": "Arma corpo a corpo recebe bônus em testes de ataque e margem de ameaça.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Armadura de Sangue", "img": "armadura-de-sangue.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Recobre o corpo com placas de sangue endurecido.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Cinerária", "img": "cineraria.png", "elemento": "Medo", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Névoa fortalece rituais na área.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Coincidência Forçada", "img": "coincidencia-forcada.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Recebe bônus em testes.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Compreensão Paranormal", "img": "compreensao-paranormal.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você entende qualquer linguagem escrita ou falada.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Consumir Manancial", "img": "consumir-manancial.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Suga o tempo de vida de seres próximos, recebendo PV temporários.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Corpo Adaptado", "img": "corpo-adaptado.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Ignora frio e calor, pode respirar debaixo d'água.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Definhar", "img": "definhar.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Alvo fica fatigado ou vulnerável.(Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Distorcer Aparência", "img": "distorcer-aparencia.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Muda a aparência de um ou mais alvos.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Embaralhar", "img": "embaralhar.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Cria duplicatas para confundir os inimigos.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Enfeitiçar", "img": "enfeiticar.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Alvo se torna prestativo.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Fortalecimento Sensorial", "img": "fortalecimento-sensorial.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Melhora seus sentidos e sua percepção.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Luz", "img": "luz.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc": "Objeto brilha como uma lâmpada.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Nuvem de Cinzas", "img": "nuvem-de-cinzas.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Nuvem fornece camuflagem.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Ódio Incontrolável", "img": "odio-incontrolavel.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Aumenta dano corpo a corpo e perícias físicas.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Ouvir os Sussurros", "img": "ouvir-os-sussurros.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você se comunica com vozes do Outro Lado.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Polarização Caótica", "img": "polarizacao-caotica.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Objetos metálicos são atraídos ou repelidos.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Tecer Ilusão", "img": "tecer-ilusao.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Cria uma ilusão visual ou sonora.(Para melhor descrição abra o livro de regras na página 140)"},
    {"nome": "Terceiro Olho", "img": "terceiro-olho.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você vê manifestações paranormais.(Para melhor descrição abra o livro de regras na página 141)"},

    # --- 2º CÍRCULO (2 PE) ---
    {"nome": "Aprimorar Físico", "img": "aprimorar-fisico.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Bônus em Agilidade ou Força.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Aprimorar Mente", "img": "aprimorar-mente.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Fornece bônus em Intelecto ou Presença.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Chamas do Caos", "img": "chamas-do-caos.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2, "desc": "Controla o fogo.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Contenção Fantasmagórica", "img": "contencao-fantasmagorica.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Laços de energia prendem o alvo.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Detecção de Ameaças", "img": "deteccao-de-ameacas.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Detecta seres hostis e armadilhas na área.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Dissonância Acústica", "img": "dissonancia-acustica.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Cria uma área em que é impossível ouvir sons.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Esconder os Olhos", "img": "esconder-os-olhos.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Torna o usuário invisível aos olhos comuns por determinado tempo.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Flagelo de Sangue", "img": "flagelo-de-sangue.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo precisa obedecer uma ordem.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Localização", "img": "localizacao.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Determina a direção de um objeto ou ser.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Miasma Entrópico", "img": "miasma-entropico.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Nuvem tóxica enjoa e sufoca os alvos.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Paradoxo", "img": "paradoxo.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Cria uma área de tempo capaz de envelhecer corpo e alma.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Proteção contra Rituais", "img": "protecao-contra-rituais.png", "elemento": "Medo", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo recebe resistência contra efeitos paranormais.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Rejeitar Névoa", "img": "rejeitar-nevoa.png", "elemento": "Medo", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Enfraquece a conjuração de rituais.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Sopro do Caos", "img": "sopro-do-caos.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Move o ar de formas impossíveis.(Para melhor descrição abra o livro de regras na página 140)"},
    {"nome": "Transfusão Vital", "img": "transfusao-vital.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Transfere vida do usuário para um ser.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Velocidade Mortal", "img": "velocidade-mortal.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo acelera no tempo, realizando ações adicionais.(Para melhor descrição abra o livro de regras na página 142)"},

    # --- 3º CÍRCULO (3 PE) ---
    {"nome": "Alterar Memória", "img": "alterar-memoria.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Pode apagar ou modificar a memória recente do alvo.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Âncora Temporal", "img": "ancora-temporal.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Impede o alvo de se afastar de um ponto.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Contato Paranormal", "img": "contato-paranormal.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Você barganha com o Outro Lado para obter ajuda.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Convocação Instantânea", "img": "convocacao-instantanea.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Teletransporta um objeto marcado para suas mãos.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Dissipar Ritual", "img": "dissipar-ritual.png", "elemento": "Medo", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Cancela os efeitos de rituais em um alvo ou área.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Forma Monstruosa", "img": "forma-monstruosa.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Você assume a aparência de uma criatura monstruosa.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Poeira da Podridão", "img": "poeira-da-podridao.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Nuvem de poeira apodrece tudo que toca.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Transfigurar Água", "img": "transfigurar-agua.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Água e gelo se comportam de forma caótica.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Transfigurar Terra", "img": "transfigurar-terra.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Rochas, lama e areia se comportam de forma caótica.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Vidência", "img": "videncia.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Pode observar e ouvir um alvo à distância.(Para melhor descrição abra o livro de regras na página 143)"},
    {"nome": "Vomitar Pestes", "img": "vomitar-pestes.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Vomita um enxame de pequenas criaturas de Sangue.(Para melhor descrição abra o livro de regras na página 143)"},

    # --- 4º CÍRCULO (4 PE) ---
    {"nome": "Alterar Destino", "img": "alterar-destino.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Enxerga o futuro próximo, podendo alterar um resultado.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Canalizar o Medo", "img": "canalizar-o-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Transfere parte de seu poder paranormal para um alvo.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Capturar o Coração", "img": "capturar-o-coracao.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Manipula as emoções e vontades do alvo.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Conhecendo o Medo", "img": "conhecendo-o-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Manifesta o Medo absoluto na mente do alvo.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Controle Mental", "img": "controle-mental.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Faz com que a mente da vítima seja controlada.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Convocar o Algoz","img": "convocar-o-algoz.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Conjura o maior medo do alvo para persegui-lo.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Distorção Temporal", "img": "distorcao-temporal.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você age livremente por um curto período de tempo."},
    {"nome": "Fim Inevitável", "img": "fim-inevitavel.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Abre uma ruptura no espaço que suga tudo ao redor.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Inexistir", "img": "inexistir.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você toca um alvo e o apaga da existência.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Invólucro de Carne", "img": "involucro-de-carne.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Cria um clone de carne e sangue.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Lâmina do Medo", "img": "lamina-do-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Golpeia o alvo com uma lâmina de medo puro.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Medo Tangível", "img": "medo-tangivel.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Recebe uma série de imunidades paranormais.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Possessão", "img": "possessao.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Transfere sua consciência para o corpo do alvo.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Presença do Medo", "img": "presenca-do-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você assume uma forma impossível dentro da realidade.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Teletransporte", "img": "teletransporte.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Teletransporta você e outros seres.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Vínculo de Sangue", "img": "vinculo-de-sangue.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Alvo sofre todo dano que você sofrer.(Para melhor descrição abra o livro de regras na página 143)"},
]

# 3. UNIÃO DAS LISTAS PARA A GALERIA
# O Python soma as duas listas automaticamente para criar a biblioteca completa.
todos_rituais = meu_deck + catalogo_geral

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sorteador')
def sorteador():
    return render_template('index.html')

@app.route('/galeria')
def galeria():
    # A Galeria recebe a lista COMPLETA (todos_rituais)
    return render_template('galeria.html', rituais=todos_rituais)

@app.route('/erro')
def erro():
    return render_template('erro.html')

@app.route('/sortear')
def sortear():
    # O Sorteador puxa APENAS do seu deck pessoal
    return jsonify(random.choice(meu_deck))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)