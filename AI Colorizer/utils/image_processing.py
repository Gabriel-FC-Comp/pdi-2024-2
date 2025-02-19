"""
Módulo para processamento de imagens em escala de cinza e integração com o modelo de colorização.

Este módulo contém funções para:
- Verificar se uma imagem está em escala de cinza.
- Decodificar imagens recebidas via upload.
- Preparar imagens para entrada no modelo de IA.
- Pós-processar imagens colorizadas antes do envio.
- Realizar todo o fluxo de processamento de uma imagem usando um modelo de colorização.

Módulos utilizados:
    - cv2: Para operações de manipulação de imagens.
    - numpy: Para operações matriciais.
    - typing: Para anotações de tipo.
    - ai_model: Para aplicar a colorização na imagem.

Constantes:
    - _IMG_MODEL_SIZE (tuple): Dimensão da entrada do modelo de colorização.

Funções:
    - is_image_gray_scale(img): Verifica se uma imagem está em escala de cinza.
    - decode_file_image(file): Converte um arquivo de imagem para um array numpy.
    - pre_process_image_to_model(gray_img): Prepara a imagem para ser processada pelo modelo de IA.
    - pos_process_image_to_send(colored_img, original_image_shape): Redimensiona e codifica a imagem após a colorização.
    - process_img(img_file, colorization_model): Executa todo o pipeline de processamento da imagem.

Autor:
    Gabriel Finger Conte
"""

#===============================================================================
# Importando módulos/pacotes necessários
#===============================================================================

from cv2 import imdecode, IMREAD_COLOR, cvtColor, COLOR_BGR2GRAY, COLOR_GRAY2RGB, resize, imencode
from numpy import ndarray, all, frombuffer, uint8, float32
from typing import Tuple, Union
from ai_model import colorize_img
from base64 import b64encode
from torch import device, from_numpy, Tensor
from torch.cuda import is_available
from cv2 import COLOR_RGB2BGR

#===============================================================================
# Definindo as funções do módulo atual
#===============================================================================

# Tamanho da imagem aceita pelo modelo de colorização
_IMG_MODEL_SIZE = (224,224)
# Define o dispositivo que o modelo estará rodando
curr_device = device("cuda:0" if is_available() else "cpu")

def is_image_gray_scale(img: ndarray) -> bool:
    """
    Verifica se uma imagem está em escala de cinza.

    A função considera uma imagem como escala de cinza se todos os seus canais de cor forem idênticos.

    Args:
        img (numpy.ndarray): Imagem carregada como um array numpy.

    Returns:
        bool: True se a imagem for em escala de cinza, False caso contrário.
    """
    if img.shape[2] == 3:  
        return all(img[:, :, 0] == img[:, :, 1]) and all(img[:, :, 0] == img[:, :, 2])
    return True

def decode_file_image(file):
    """
    Decodifica um arquivo de imagem para um array numpy.

    Converte a imagem enviada pelo usuário para um array numpy no formato escala de cinza, 
    caso seja colorida.

    Args:
        file (werkzeug.datastructures.FileStorage): Arquivo da imagem recebido via upload.

    Returns:
        numpy.ndarray: Imagem processada em escala de cinza.
    """
    img_bytes = file.read()
    img_array = frombuffer(img_bytes, uint8)
    img = imdecode(img_array, IMREAD_COLOR)
    
    if not is_image_gray_scale(img):
        img = cvtColor(img, COLOR_BGR2GRAY)
    
    return img

def pre_process_image_to_model(gray_img: ndarray) -> Tuple[Tensor, Tuple[int, int, int]]:
    """
    Prepara uma imagem em escala de cinza para ser processada pelo modelo de IA.

    - Converte a imagem para formato RGB (duplicando os canais).
    - Redimensiona a imagem para o tamanho esperado pelo modelo.
    - Adiciona uma dimensão extra para indicar um lote de tamanho 1.
    """
    print(gray_img.shape)
    if len(gray_img.shape) == 2:
        gray_img = cvtColor(gray_img, COLOR_GRAY2RGB)
    original_image_shape = gray_img.shape[:2][::-1]
    gray_img = resize(gray_img, _IMG_MODEL_SIZE).astype(float32)
    gray_img = gray_img.transpose(2,0,1)
    gray_img = from_numpy(gray_img).unsqueeze(0).to(curr_device)
    gray_img = (gray_img / 127.5) - 1
    return gray_img, original_image_shape

def pos_process_image_to_send(colored_img: ndarray, original_image_shape: Tuple[int, int, int]) -> Tuple[bool, Union[bytes, str]]:
    """
    Redimensiona e codifica a imagem colorizada para ser enviada via resposta HTTP.
    """
    colored_img = cvtColor(colored_img,COLOR_RGB2BGR)
    colored_img = resize(colored_img, original_image_shape)
    success, colored_img_bytes = imencode('.png', colored_img)

    if success:
        img_base64 = b64encode(colored_img_bytes).decode('utf-8')
        return (success, img_base64)
    else:
        return (False, "Erro ao codificar a imagem em PNG.")

def process_img(img_file, colorization_model) -> Tuple[bool, Union[str, ndarray]]:
    """
    Executa todo o pipeline de processamento da imagem.
    """
    gray_img = decode_file_image(img_file)
    gray_img, original_image_shape = pre_process_image_to_model(gray_img)
    colored_img = colorize_img(gray_img, colorization_model)
    success, colored_img_bytes = pos_process_image_to_send(colored_img, original_image_shape)
    if success:
        return (success, colored_img_bytes)
    else:
        return (False, 'Erro ao codificar a imagem em PNG.')
