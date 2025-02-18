"""
Módulo de redes neurais para colorização de imagens usando U-Net baseada na ResNet-18.

Este módulo define uma arquitetura de rede neural para colorização de imagens
em tons de cinza, utilizando um encoder baseado na ResNet-18 e um decoder
com blocos de convolução transposta para reconstrução das cores.

Classes principais:
- `ResNet18Encoder`: Extrai features da imagem em diferentes escalas.
- `DecoderBlock`: Realiza upsampling e combinação com skip connections.
- `UResNet18`: Implementa a arquitetura completa com encoder-decoder.

Módulos utilizados:
    - torch: Framework para deep learning.
    - torch.nn: Implementa camadas de redes neurais.
    - torchvision.models: Contém modelos pré-treinados, como a ResNet-18.

Autor:
    Gabriel Finger Conte
"""

#===============================================================================
# Importando módulos/pacotes necessários
#===============================================================================

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet18_Weights

#===============================================================================
# Definindo as funções do módulo atual
#===============================================================================

class ResNet18Encoder(nn.Module):
    """
    Encoder baseado na ResNet-18 para extração de features.

    A ResNet-18 é utilizada como extratora de features, congelando seus pesos
    e separando suas camadas principais para uso no encoder da U-Net.
    """
    def __init__(self):
        super().__init__()
        resnet = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        for param in resnet.parameters():
            param.requires_grad = False

        self.conv1 = resnet.conv1
        self.bn1 = resnet.bn1
        self.relu = resnet.relu
        self.maxpool = resnet.maxpool
        
        self.layer1 = resnet.layer1  # Saída: 64x56x56
        self.layer2 = resnet.layer2  # Saída: 128x28x28
        self.layer3 = resnet.layer3  # Saída: 256x14x14
        self.layer4 = resnet.layer4  # Saída: 512x7x7

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor]:
        """
        Executa o forward pass e retorna as features extraídas.

        Args:
            x (torch.Tensor): Tensor de entrada com dimensão (B, C, H, W).

        Returns:
            Tuple[torch.Tensor]: Features extraídas em diferentes resoluções.
        """
        x0 = self.relu(self.bn1(self.conv1(x)))  # 64x112x112
        x1 = self.maxpool(x0)                    # 64x56x56
        
        x2 = self.layer1(x1)  # 64x56x56
        x3 = self.layer2(x2)  # 128x28x28
        x4 = self.layer3(x3)  # 256x14x14
        x5 = self.layer4(x4)  # 512x7x7
        
        return x0, x2, x3, x4, x5
    
class DecoderBlock(nn.Module):
    """
    Bloco de decodificação para a U-Net, utilizando upsampling e skip connections.
    """
    def __init__(self, in_channels, out_channels, skip_channels, dropout_rate=0.2):
        super().__init__()
        self.up = nn.ConvTranspose2d(
            in_channels, out_channels, 
            kernel_size=3, stride=2, 
            padding=1, output_padding=1
        )
        self.conv = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Conv2d(out_channels + skip_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x, skip) -> torch.Tensor:
        """
        Realiza upsampling e combinação com as features do encoder.
        
        Args:
            x (torch.Tensor): Tensor de entrada com dimensão (B, C, H, W).
            skip (torch.Tensor): Tensor de complementar de entrada, 
                fruto de uma camada intermediária do encoder, com dimensão (B, C, H, W).

        Returns:
            torch.Tensor: Features extraídas, com dimensão (B, C, H, W).
        """
        x = self.up(x)
        x = torch.cat([x, skip], dim=1)
        x = self.conv(x)
        return x
    
class UResNet18(nn.Module):
    """
    Arquitetura de colorização baseada em U-Net com ResNet-18 como encoder.
    """
    def __init__(self):
        super().__init__()
        self.encoder = ResNet18Encoder()
        
        self.decoder4 = DecoderBlock(512, 256, 256)  # 7x7 → 14x14
        self.decoder3 = DecoderBlock(256, 128, 128)  # 14x14 → 28x28
        self.decoder2 = DecoderBlock(128, 64, 64)    # 28x28 → 56x56
        self.decoder1 = DecoderBlock(64, 64, 64)     # 56x56 → 112x112
        
        self.final_upsample = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 3, kernel_size=1),  # Saída RGB
            nn.Sigmoid()
        )
        
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, x) -> torch.Tensor:
        """
        Executa o forward pass na rede U-Net.
        Args:
            x (torch.Tensor): Tensor de entrada com dimensão (B, C, H, W).

        Returns:
            torch.Tensor: Features extraídas, com dimensão (B, C, H, W).
        """
        s0, s1, s2, s3, s4 = self.encoder(x)
        d4 = self.decoder4(s4, s3)
        d3 = self.decoder3(d4, s2)
        d2 = self.decoder2(d3, s1)
        d1 = self.decoder1(d2, s0)
        return self.final_upsample(d1)
    
    def predict(self, x) -> torch.Tensor:
        """
        Realiza a inferência na imagem de entrada.
        Args:
            x (torch.Tensor): Tensor de entrada com dimensão (B, C, H, W).

        Returns:
            torch.Tensor: Features extraídas, sem manter tracking do gradiente, com dimensão (B, C, H, W).
        """
        self.eval()
        with torch.inference_mode():
            return self(x)
