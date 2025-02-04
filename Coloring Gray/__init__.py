#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# Importando módulos/pacotes
#===============================================================================

from flask import Flask, render_template,request, jsonify#, send_file
from flask_socketio import SocketIO#, emit  
import numpy as np
import cv2
# import os

#===============================================================================
# Configurações do Servidor
#===============================================================================

# Inicializando o Flask com WebSocket
app = Flask(__name__)
socketio = SocketIO(app)

#===============================================================================
# Configurando utils (Será separado em módulos distintos posteriormente)
#===============================================================================

# os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def decode_file_image(file):
    # Lê os bytes da imagem
    img_bytes = file.read()

    # Converte os bytes em um array numpy
    img_array = np.frombuffer(img_bytes, np.uint8)

    # Decodifica a imagem (como se fosse o cv2.imread)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img

#===============================================================================
# Configurando rotas
#===============================================================================

# Definindo a rota principal
@app.route('/')
def homepage():
    """ Renderiza o modelo HTML da página inicial """
    return render_template('homepage.html')  

@app.route('/upload', methods=['POST'])
def upload_file():
    """ Obtém a imagem enviada pelo cliente via POST """
    if 'gray_image_file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado!"}), 400

    # Pega o arquivo da requisição
    file = request.files['gray_image_file']
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo não detectado!"}), 400

    return jsonify({"message": f"Arquivo {file.filename} recebido com sucesso!"}), 200

#===============================================================================
# Inicializando o app
#===============================================================================

if __name__ == "__main__":
    # Inicia o servidor Flask com suporte a WebSocket
    socketio.run(app, debug=True, port=8001, host='127.0.0.1')