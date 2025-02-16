#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo principal da aplicação Flask para colorização de imagens.

Este módulo inicializa o servidor Flask, configura as rotas principais e carrega o modelo
de aprendizado de máquina para colorização de imagens.

A aplicação fornece as seguintes funcionalidades:
- Renderização da página inicial via Flask (`/`).
- Endpoint para upload e processamento de imagens em escala de cinza (`/upload`).
- Integração com um modelo de IA para colorização de imagens.
- Verificação da carga correta do modelo de IA antes de iniciar o servidor.

Módulos utilizados:
    - flask: Para criação da API web.
    - os: Para manipulação de processos e caminhos.
    - sys: Para modificação do caminho de importação de módulos.
    - utils.image_processing: Contém funções de processamento de imagens.
    - utils.ai_model: Responsável pela importação do modelo treinado.

Autor:
    Gabriel Finger Conte
"""

#===============================================================================
# Importando módulos/pacotes
#===============================================================================

from sys import path
from os.path import join, abspath
from flask import Flask, render_template, request, jsonify
from os import kill, getpid

# Adicionando ao PATH o diretório dos utilitários para importação
path.append(abspath(join(Flask(__name__).root_path, 'utils')))

from utils.image_processing import process_img
from utils.ai_model import import_model_resnet18

#===============================================================================
# Configurações do Servidor
#===============================================================================

# Inicializando o Flask
app = Flask(__name__)

# Definindo diretório estático
static_folder = join(app.root_path, 'static')

# Instanciando o modelo treinado para colorização de imagens
colorization_model = import_model_resnet18(static_folder)
if colorization_model is None:
    print("Erro ao carregar o modelo. Desligando servidor...")
    kill(getpid(), 9)

#===============================================================================
# Configurando rotas
#===============================================================================

@app.route('/')
def homepage():
    """
    Renderiza a página inicial da aplicação.

    Returns:
        str: O HTML renderizado da página inicial.
    """
    return render_template('homepage.html')  

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Rota para upload e processamento de imagens.

    Args:
        Nenhum argumento explícito; os dados são passados via `request.files`.

    Returns:
        JSON: Um dicionário JSON com a mensagem de sucesso ou erro e o código HTTP correspondente.
    
    Responses:
        200: {"message": "Imagem <nome> recebida e processada com sucesso!", "file": <dados_da_imagem>}
        400: {"error": "Nenhum arquivo enviado!"} ou {"error": "Nome do arquivo não detectado!"} ou {"error": "<mensagem_erro>"}
    """
    
    if 'gray_image_file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado!"}), 400

    file = request.files['gray_image_file']
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo não detectado!"}), 400

    # Tenta processar e colorir a imagem
    success, content = process_img(file, colorization_model)
    
    if success:
        return jsonify({"message": f"Imagem {file.filename} recebida e processada com sucesso!", "file": content}), 200
    else:
        return jsonify({"error": f"{content}"}), 400

#===============================================================================
# Inicializando o app
#===============================================================================

if __name__ == "__main__":
    app.run(debug=True, port=8001, host='127.0.0.1')
