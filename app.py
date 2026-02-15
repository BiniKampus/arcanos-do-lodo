from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Aqui é o seu estoque de cartas.
# "img" precisa ser o nome exato da imagem que está na pasta 'static'
meu_deck = [
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"}
    #{"nome": "Florescer Caótico", "img": "florescer-caotico.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":Quando não se sabe o que fazer, deixe na mão do Outro Lado. Três raios saem do seu peito e acertam alvos aleatórios a sua volta, para cada raio você deve rolar um d20, caso o resultado sair 10 ou menor ele acerta um aliado (a critério do mestre) e caso seja maior acerta um inimigo a sua escolha, caso não haja alvos disponíveis, o disparo é descartado. Um inimigo não pode ser acertado por mais de um raio. O raio causa 3d10+5 de Energia."}
    {"nome": "Cauterização Caótica", "img": "cicatrizacao.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Estática e efeitos luminosos e sonoros surgem ao redor de um alvo. O alvo recupera 1d6+1 PV no início do turno dele, mas o caos adora se divertir, ao receber a cura também role 1d6 para um dos efeitos a seguir. Usar novamente dissipar uso anterior. (1): Dobra a quantidade de cura recebida. (2): O alvo fica ofuscado até o início do próximo turno. (3): Causa +1d6 de dano de energia no seu primeiro ataque da rodada. (4): O alvo não pode usar reações especiais até o início do próximo turno. (5): Recebe +2 no teste de acerto e -2 de Defesa e RD. (6): O alvo não pode gastar PD até o início do próximo turno."}
    {"nome": "Coincidência Forçada", "img": "coincidencia-forcada.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc": "Recebe bônus em testes.(Para melhor descrição abra o livro de regras na página 126)"}
    {"nome": "Eletrocussão", "img": "eletrocussao.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Corrente voltaica eletrocuta o alvo.(Para melhor descrição abra o livro de regras na página 131)"}
]
meu_deck_80 = [
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png","fonte": "livro", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Cicatrização", "img": "cicatrizacao.png","fonte": "livro", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Você acelera o tempo ao redor das feridas do alvo, que cicatrizam instantaneamente. O alvo recupera 3d8+3 PV, mas envelhece 1 ano automaticamente.. (Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Decadência", "img": "decadencia.png","fonte": "livro", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Espirais de trevas envolvem sua mão e definham o alvo, que sofre 2d8+2 pontos de dano de Morte. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Deflagração de Energia", "img": "deflagracao-de-energia.png","fonte": "livro", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4, "desc":"Você acumula uma quantidade imensa de Energia, então a libera em uma explosão intensa, como uma estrela em plena terra. Todos na área sofrem 3d10 x 10 pontos de dano de Energia (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Desacelerar Impacto", "img": "desacelerar-impacto.png","fonte": "livro", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2, "desc":"O alvo cai lentamente. A velocidade da queda é reduzida para 18m por rodada — o suficiente para não causar dano. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Descarnar", "img": "descarnar.png","fonte": "livro", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2, "desc":"A pele do alvo é dilacerada, abrindo cortes profundos. (Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Eco Espiral", "img": "eco-espiral.png","fonte": "livro", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2, "desc":"Repete o dano que o alvo sofreu ao longo das rodadas concentrando. (Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Eletrocussão", "img": "eletrocussao.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Corrente voltaica eletrocuta o alvo.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Espirais da Perdição", "img": "espirais-da-perdicao.png","fonte": "livro", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1, "desc":"Inimigos sofrem penalidade em ataque.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Ferver Sangue", "img": "ferver-sangue.png","fonte": "livro", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3, "desc":"Faz o sangue do alvo entrar em ebulição, causando dano e deixando-o fraco.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Hemofagia", "img": "hemofagia.png","fonte": "livro", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2, "desc":"Absorve o sangue do alvo, causando dano e recuperando seus pontos de vida.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Invadir Mente", "img": "invadir-mente.png","fonte": "livro", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2, "desc":"Gera uma rajada mental ou se conecta telepaticamente.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Mergulho Mental", "img": "mergulho-mental.png","fonte": "livro", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3, "desc":"Se infiltra na mente do alvo para vasculhar seus pensamentos.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Perturbação", "img": "perturbacao.png","fonte": "livro", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1, "desc":"Força o alvo a obedecer a uma ordem.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Purgatório", "img": "purgatorio.png","fonte": "livro", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3, "desc":"Área de sangue deixa alvos vulneráveis a dano e causa dor a quem tentar sair.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Salto Fantasma", "img": "salto-fantasma.png","fonte": "livro", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3, "desc":"Teletransporta você e outros seres para um ponto dentro do alcance.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Tela de Ruído", "img": "tela-de-ruido.png","fonte": "livro", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2, "desc":"Cria uma película protetora que absorve dano.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Tentáculos de Lodo", "img": "tentaculos-de-lodo.png","fonte": "livro", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3, "desc":"Tentáculos pretos atacam e agarram seres na área.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Zerar Entropia", "img": "zerar-entropia.png","fonte": "livro", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3, "desc":"O alvo fica lento ou paralisado.(Para melhor descrição abra o livro de regras na página 143)"},
]

catalogo_geral = [
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png","fonte": "livro", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Arma", "img": "AmaldiçoarArma.png","fonte": "livro", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1, "desc":"Você imbui a arma ou munições com o elemento, fazendo com que causem +1d6 de dano do tipo do elemento. (Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Amaldiçoar Tecnologia","invertir": True, "img": "amaldicoar-tecnologia.png","fonte": "livro", "circulo": "1ºCírculo", "elemento": "Energia", "pe": 1,
     "desc": "Aprimora um item.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Arma Atroz", "img": "arma-atroz.png","fonte": "livro", "circulo": "1ºCírculo", "elemento": "Sangue", "pe": 1,
     "desc": "Arma corpo a corpo recebe bônus em testes de ataque e margem de ameaça.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Armadura de Sangue", "img": "armadura-de-sangue.png","fonte": "livro", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Recobre o corpo com placas de sangue endurecido.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Cinerária", "img": "cineraria.png","fonte": "livro", "elemento": "Medo", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Névoa fortalece rituais na área.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Coincidência Forçada", "img": "coincidencia-forcada.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Recebe bônus em testes.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Compreensão Paranormal","fonte": "livro", "img": "compreensao-paranormal.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você entende qualquer linguagem escrita ou falada.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Consumir Manancial","fonte": "livro", "img": "consumir-manancial.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Suga o tempo de vida de seres próximos, recebendo PV temporários.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Corpo Adaptado","fonte": "livro", "img": "corpo-adaptado.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Ignora frio e calor, pode respirar debaixo d'água.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Definhar","fonte": "livro", "img": "definhar.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Alvo fica fatigado ou vulnerável.(Para melhor descrição abra o livro de regras na página 129)"},
    {"nome": "Distorcer Aparência","fonte": "livro", "img": "distorcer-aparencia.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Muda a aparência de um ou mais alvos.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Embaralhar","fonte": "livro", "img": "embaralhar.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Cria duplicatas para confundir os inimigos.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Enfeitiçar","fonte": "livro", "img": "enfeiticar.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Alvo se torna prestativo.(Para melhor descrição abra o livro de regras na página 131)"},
    {"nome": "Fortalecimento Sensorial","fonte": "livro", "img": "fortalecimento-sensorial.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Melhora seus sentidos e sua percepção.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Luz", "img": "luz.png","fonte": "livro", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1, "desc": "Objeto brilha como uma lâmpada.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Nuvem de Cinzas","fonte": "livro", "img": "nuvem-de-cinzas.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Nuvem fornece camuflagem.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Ódio Incontrolável","fonte": "livro", "img": "odio-incontrolavel.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Aumenta dano corpo a corpo e perícias físicas.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Ouvir os Sussurros","fonte": "livro", "img": "ouvir-os-sussurros.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você se comunica com vozes do Outro Lado.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Polarização Caótica","fonte": "livro", "img": "polarizacao-caotica.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Objetos metálicos são atraídos ou repelidos.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Tecer Ilusão","fonte": "livro", "img": "tecer-ilusao.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Cria uma ilusão visual ou sonora.(Para melhor descrição abra o livro de regras na página 140)"},
    {"nome": "Terceiro Olho","fonte": "livro", "img": "terceiro-olho.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você vê manifestações paranormais.(Para melhor descrição abra o livro de regras na página 141)"},

    # --- 2º CÍRCULO (2 PE) ---
    {"nome": "Aprimorar Físico","fonte": "livro", "img": "aprimorar-fisico.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Bônus em Agilidade ou Força.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Aprimorar Mente","fonte": "livro", "img": "aprimorar-mente.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Fornece bônus em Intelecto ou Presença.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Chamas do Caos","fonte": "livro", "img": "chamas-do-caos.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2, "desc": "Controla o fogo.(Para melhor descrição abra o livro de regras na página 126)"},
    {"nome": "Contenção Fantasmagórica","fonte": "livro", "img": "contencao-fantasmagorica.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Laços de energia prendem o alvo.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Detecção de Ameaças","invertir": True,"fonte": "livro", "img": "deteccao-de-ameacas.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Detecta seres hostis e armadilhas na área.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Dissonância Acústica","fonte": "livro", "img": "dissonancia-acustica.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Cria uma área em que é impossível ouvir sons.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Esconder os Olhos","fonte": "livro", "img": "esconder-os-olhos.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Torna o usuário invisível aos olhos comuns por determinado tempo.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Flagelo de Sangue","fonte": "livro", "img": "flagelo-de-sangue.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo precisa obedecer uma ordem.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Localização","fonte": "livro", "img": "localizacao.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Determina a direção de um objeto ou ser.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Miasma Entrópico","fonte": "livro", "img": "miasma-entropico.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Nuvem tóxica enjoa e sufoca os alvos.(Para melhor descrição abra o livro de regras na página 136)"},
    {"nome": "Paradoxo","fonte": "livro", "img": "paradoxo.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Cria uma área de tempo capaz de envelhecer corpo e alma.(Para melhor descrição abra o livro de regras na página 137)"},
    {"nome": "Proteção contra Rituais","fonte": "livro", "img": "protecao-contra-rituais.png", "elemento": "Medo", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo recebe resistência contra efeitos paranormais.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Rejeitar Névoa","fonte": "livro", "img": "rejeitar-nevoa.png", "elemento": "Medo", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Enfraquece a conjuração de rituais.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Sopro do Caos","invertir": True,"fonte": "livro", "img": "sopro-do-caos.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Move o ar de formas impossíveis.(Para melhor descrição abra o livro de regras na página 140)"},
    {"nome": "Transfusão Vital","fonte": "livro", "img": "transfusao-vital.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Transfere vida do usuário para um ser.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Velocidade Mortal","invertir": True,"fonte": "livro", "img": "velocidade-mortal.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Alvo acelera no tempo, realizando ações adicionais.(Para melhor descrição abra o livro de regras na página 142)"},

    # --- 3º CÍRCULO (3 PE) ---
    {"nome": "Alterar Memória", "img": "alterar-memoria.png", "fonte": "livro", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Pode apagar ou modificar a memória recente do alvo.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Âncora Temporal","fonte": "livro", "img": "ancora-temporal.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Impede o alvo de se afastar de um ponto.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Contato Paranormal","fonte": "livro", "img": "contato-paranormal.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Você barganha com o Outro Lado para obter ajuda.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Convocação Instantânea","fonte": "livro", "img": "convocacao-instantanea.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Teletransporta um objeto marcado para suas mãos.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Dissipar Ritual","invertir": True,"fonte": "livro", "img": "dissipar-ritual.png", "elemento": "Medo", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Cancela os efeitos de rituais em um alvo ou área.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Forma Monstruosa","fonte": "livro", "img": "forma-monstruosa.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Você assume a aparência de uma criatura monstruosa.(Para melhor descrição abra o livro de regras na página 133)"},
    {"nome": "Poeira da Podridão","invertir": True,"fonte": "livro", "img": "poeira-da-podridao.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Nuvem de poeira apodrece tudo que toca.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Transfigurar Água","fonte": "livro", "img": "transfigurar-agua.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Água e gelo se comportam de forma caótica.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Transfigurar Terra","invertir": True,"fonte": "livro", "img": "transfigurar-terra.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Rochas, lama e areia se comportam de forma caótica.(Para melhor descrição abra o livro de regras na página 142)"},
    {"nome": "Vidência","fonte": "livro", "img": "videncia.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Pode observar e ouvir um alvo à distância.(Para melhor descrição abra o livro de regras na página 143)"},
    {"nome": "Vomitar Pestes","fonte": "livro", "img": "vomitar-pestes.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Vomita um enxame de pequenas criaturas de Sangue.(Para melhor descrição abra o livro de regras na página 143)"},

    # --- 4º CÍRCULO (4 PE) ---
    {"nome": "Alterar Destino","fonte": "livro", "img": "alterar-destino.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Enxerga o futuro próximo, podendo alterar um resultado.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Canalizar o Medo","fonte": "livro", "img": "canalizar-o-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Transfere parte de seu poder paranormal para um alvo.(Para melhor descrição abra o livro de regras na página 125)"},
    {"nome": "Capturar o Coração","fonte": "livro", "img": "capturar-o-coracao.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Manipula as emoções e vontades do alvo.(Para melhor descrição abra o livro de regras na página 124)"},
    {"nome": "Conhecendo o Medo","fonte": "livro", "img": "conhecendo-o-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Manifesta o Medo absoluto na mente do alvo.(Para melhor descrição abra o livro de regras na página 127)"},
    {"nome": "Controle Mental","fonte": "livro", "img": "controle-mental.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Faz com que a mente da vítima seja controlada.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Convocar o Algoz","invertir": True,"onte": "livro","img": "convocar-o-algoz.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Conjura o maior medo do alvo para persegui-lo.(Para melhor descrição abra o livro de regras na página 128)"},
    {"nome": "Distorção Temporal","fonte": "livro", "img": "distorcao-temporal.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você age livremente por um curto período de tempo.(Para melhor descrição abra o livro de regras na página 130)"},
    {"nome": "Fim Inevitável","fonte": "livro", "img": "fim-inevitavel.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Abre uma ruptura no espaço que suga tudo ao redor.(Para melhor descrição abra o livro de regras na página 132)"},
    {"nome": "Inexistir", "fonte": "livro","img": "inexistir.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você toca um alvo e o apaga da existência.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Invólucro de Carne","fonte": "livro", "img": "involucro-de-carne.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Cria um clone de carne e sangue.(Para melhor descrição abra o livro de regras na página 134)"},
    {"nome": "Lâmina do Medo","fonte": "livro", "img": "lamina-do-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Golpeia o alvo com uma lâmina de medo puro.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Medo Tangível","fonte": "livro", "img": "medo-tangivel.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Recebe uma série de imunidades paranormais.(Para melhor descrição abra o livro de regras na página 135)"},
    {"nome": "Possessão","fonte": "livro", "img": "possessao.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Transfere sua consciência para o corpo do alvo.(Para melhor descrição abra o livro de regras na página 138)"},
    {"nome": "Presença do Medo","fonte": "livro", "img": "presenca-do-medo.png", "elemento": "Medo", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você assume uma forma impossível dentro da realidade.(Para melhor descrição abra o livro de regras na página 139)"},
    {"nome": "Teletransporte","fonte": "livro", "img": "teletransporte.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Teletransporta você e outros seres.(Para melhor descrição abra o livro de regras na página 141)"},
    {"nome": "Vínculo de Sangue","fonte": "livro", "img": "vinculo-de-sangue.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Alvo sofre todo dano que você sofrer.(Para melhor descrição abra o livro de regras na página 143)"},

    # --- SOBREVIVENDO AO HORROR / 1º CÍRCULO (1PE)
    {"nome": "Esfolar","invertir": True, "fonte": "horror", "img": "esfolar.png", "elemento": "Sangue", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Você usa seu corpo como passagem para o Sangue, projetando agulhas e lâminas rubras praticamente imperceptíveis que se projetam contra o alvo. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 48)"},
    {"nome": "Apagar as Luzes","invertir": True, "fonte": "horror", "img": "apagar-as-luzes.png", "elemento": "Morte", "circulo": "1ºCírculo", "pe": 1,
     "desc": "qualquer fonte de luz em alcance curto de você, natural ou paranormal, se apaga. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 50)"},
    {"nome": "Desfazer Sinapses","invertir": True, "fonte": "horror", "img": "desfazer-sinapses.png", "elemento": "Conhecimento", "circulo": "1ºCírculo", "pe": 1,
     "desc": "A entidade do Conhecimento inexiste bilhões de neurônios de dentro do cérebro do alvo, causando a angústia inexplicável do vazio. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 53)"},
    {"nome": "Overclock","invertir": True, "fonte": "horror", "img": "overclock.png", "elemento": "Energia", "circulo": "1ºCírculo", "pe": 1,
     "desc": "Ao fazer um teste de Tecnologia para lidar com um objeto eletrônico, você pode, após saber se passou no teste ou não, conjurar este ritual para receber as informações que buscava de outra forma, usando descargas de Energia para forçar o aparelho a seguir suas vontades. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 55)"},

    # --- 2º CÍRCULO (2PE)
    {"nome": "Sede de Adrenalina","invertir": True, "fonte": "horror", "img": "sede-de-adrenalina.png", "elemento": "Sangue", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Quando você falha em um teste de Acrobacia ou Atletismo, pode conjurar esse ritual para repetir esse teste, usando Presença no lugar do atributo base daquela perícia. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 49)"},
    {"nome": "Lingua Morta","invertir": True, "fonte": "horror", "img": "lingua-morta.png", "elemento": "Morte", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Ao preparar um cadáver humano e conjurar esse ritual, o Lodo da Morte se espalha por dentro do cadáver, reanimando-o forçadamente. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 51)"},
    {"nome": "Aurora da Verdade","invertir": True, "fonte": "horror", "img": "aurora-da-verdade.png", "elemento": "Conhecimento", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Uma luz espectral como ondas de uma aurora boreal dourada surge na área do ritual, e qualquer ser dentro dessa área é obrigado a falar apenas a verdade, inclusive o conjurador. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 53)"},
    {"nome": "Tremeluzir","invertir": True, "fonte": "horror", "img": "tremeluzir.png", "elemento": "Energia", "circulo": "2ºCírculo", "pe": 2,
     "desc": "Enquanto estiver nesse estado, você e todo objeto que estiver carregando são capazes de atravessar objetos sólidos. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 55)"},

    # --- 3º CÍRCULO (3PE)
    {"nome": "Odor da Caçada","invertir": True, "fonte": "horror", "img": "odor-da-cacada.png", "elemento": "Sangue", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Seu nariz enruga, suas pupilas dilatam e os odores ao seu redor se intensificam. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 49)"},
    {"nome": "Fedor Pútrido","invertir": True, "fonte": "horror", "img": "fedor-putrido.png", "elemento": "Morte", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Seu coração para de bater, seus pulmões deixam de inflar, seu sangue cessa de fluir. Tudo fica, temporariamente, sendo sustentado pelo Lodo da Morte. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 52)"},
    {"nome": "Relembrar Fragmento","invertir": True, "fonte": "horror", "img": "relembrar-fragmento.png", "elemento": "Conhecimento", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Após a conjuração, o objeto é completamente restaurado para o momento em que recebeu sua última anotação e permanece assim enquanto o conjurador tocá-lo. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 54)"},
    {"nome": "Mutar","invertir": True, "fonte": "horror", "img": "mutar.png", "elemento": "Energia", "circulo": "3ºCírculo", "pe": 3,
     "desc": "Esse ritual concede +10 em testes de Furtividade e reduz qualquer ganho de visibilidade em cenas de furtividade em 1, a critério do mestre.. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 56)"},

    # --- 4º CÍRCULO (4PE)
    {"nome": "Martírio de Sangue","invertir": True, "fonte": "horror", "img": "martirio-de-sangue.png", "elemento": "Sangue", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você fica mais forte, rápido e resistente, em troca de uma mente nublada pela raiva e uma aparência animalesca, sentindo os músculos rasgando, os ossos ficando protuberantes e a sua pele endurecendo em uma estrutura de couro rubro. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 50)"},
    {"nome": "Singularidade Temporal","invertir": True, "fonte": "horror", "img": "singularidade-temporal.png", "elemento": "Morte", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você distorce a Realidade em espirais capazes de alterar as condições temporais de um objeto para avançá-lo no tempo, fazendo com que ele atinja o estado de decomposição mais avançado que um objeto do seu tipo poderia alcançar. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 52)"},
    {"nome": "Pronunciar Sigilo","invertir": True, "fonte": "horror", "img": "pronunciar-sigilo.png", "elemento": "Conhecimento", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Você profana a Realidade, pronunciando um dos Sigilos do Conhecimento em voz alta, deturpando a natureza de um ser com o poder do Outro Lado. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 54)"},
    {"nome": "Milagre Ionizante","invertir": True, "fonte": "horror", "img": "milagre-ionizante.png", "elemento": "Energia", "circulo": "4ºCírculo", "pe": 4,
     "desc": "Como um ocultista experiente, você usa de todo seu esforço para que o caos embaralhe a Realidade com o intuito de destruir apenas uma estrutura maligna habitando um corpo. (Para melhor descrição abra o suplemento Sobrevivendo ao Horror na página 56)"},

    # --- ARQUIVOS SECRETOS
    {"nome": "Passagem de Conhecimento", "invertir": True, "fonte": "arquivos", "img": "passagem-de-conhecimento.png",
     "elemento": "Sangue/Conhecimento", "circulo": "2ºCírculo", "pe": 2, "desc": "Você transfere sua consciência para o corpo do alvo. (Para melhor descrição abra o Arquivos Secretos na página 48)"},
    {"nome": "Passagem de Conhecimento Expandido", "invertir": True, "fonte": "arquivos", "img": "passagem-de-conhecimento-expandido.png",
     "elemento": "Sangue/Conhecimento", "circulo": "4ºCírculo", "pe": 4, "desc": "Dez pessoas são necessárias para esse ritual. Cinco delas serão os receptáculos e deverão estar inconscientes, enquanto as outras cinco devem ser voluntárias e terão suas consciência paranormalmente transportadas para os corpos dos receptáculos.. (Para melhor descrição abra o Arquivos Secretos na página 50)"},

]

# 3. UNIÃO DAS LISTAS PARA A GALERIA
# O Python soma as duas listas automaticamente para criar a biblioteca completa.
todos_rituais = meu_deck_80 + catalogo_geral

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