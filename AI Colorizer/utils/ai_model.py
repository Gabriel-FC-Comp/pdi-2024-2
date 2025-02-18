"""
Módulo de carregamento e uso do modelo de IA para colorização de imagens.

Este módulo fornece funções para:
- Carregar o modelo de colorização treinado a partir de um arquivo.
- Aplicar o modelo a uma imagem em escala de cinza para obter uma versão colorida.
- Reverter a normalização de imagens para o intervalo adequado de visualização.

Módulos utilizados:
    - numpy: Para manipulação de arrays numéricos.
    - torch: Para carregar o modelo e processar tensores.
    - os.path: Para manipulação de caminhos de arquivos.
    - resnet18_model: Para importar a arquitetura UResNet18 utilizada na colorização.

Funções:
    - import_model_resnet18(model_path): Carrega o modelo de colorização ResNet-18 a partir do diretório especificado.
    - reverse_normalization(img): Reverte a normalização de uma imagem do intervalo [0, 1] para [0, 255].
    - colorize_img(gray_img, model): Aplica o modelo carregado a uma imagem em escala de cinza.

Autor:
    Gabriel Finger Conte
"""

#===============================================================================
# Importando módulos/pacotes necessários
#===============================================================================

from numpy import clip, ndarray, uint8
from resnet18_model import UResNet18
from torch import load, Tensor, device
from torch.cuda import is_available
from os.path import join

#===============================================================================
# Definindo as funções do módulo atual
#===============================================================================

_model_name = 'resnet18_model_v2_250e.pth'

def import_model_resnet18(model_path: str):
    """
    Carrega o modelo de colorização treinado ResNet-18.

    Args:
        model_path (str): Caminho para o diretório contendo o modelo `.pth`.

    Returns:
        torch.nn.Module or None: O modelo carregado, ou None em caso de falha.
    """
    try:
        color_model_resnet18 = UResNet18()
        available_device = device('cuda' if is_available() else 'cpu')
        color_model_resnet18.load_state_dict(load(join(model_path, _model_name),map_location=available_device))
        
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        color_model_resnet18 = None
    
    return color_model_resnet18


def reverse_normalization(img: ndarray) -> ndarray:
    """
    Reverte a normalização de uma imagem do intervalo [-1, 1] para [0, 255].

    Esta função multiplica os valores da imagem pelo fator 255, 
    garantindo que os valores fiquem no intervalo [0, 255] e os 
    converte para o tipo de dado uint8 para visualização e armazenamento adequados.

    Args:
        img (numpy.ndarray): A imagem normalizada no intervalo [-1, 1].

    Returns:
        numpy.ndarray: A imagem revertida para o intervalo [0, 255] e convertida para tipo uint8.
    """
    return clip(img * 255, 0, 255).astype(uint8)


def colorize_img(gray_img: Tensor, model) -> ndarray:
    """
    Aplica o modelo de IA a uma imagem em escala de cinza para colorização.

    Args:
        gray_img (torch.Tensor): Imagem de entrada em escala de cinza, formatada para o modelo.
        model (torch.nn.Module): Modelo treinado para colorização.

    Returns:
        numpy.ndarray: Imagem colorizada com os canais RGB previstos pelo modelo.
    """
    # Colore a imagem
    colored_img = model.predict(gray_img)
    # Converte para ndarray
    colored_img = colored_img.cpu().numpy()
    # Ajusta as dimensões novamente para (Idx, H, W, C)
    colored_img = colored_img.transpose(0, 2, 3, 1)
    # Remove a dimensão extra da predição e reverte a normalização
    colored_img = reverse_normalization(colored_img[0])
    return colored_img