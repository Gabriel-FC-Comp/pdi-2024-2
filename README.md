# Processamento Digital de Imagens (2024/2)

Este repositório contém os projetos desenvolvidos na disciplina de **Processamento Digital de Imagens (2024/2)**.

## Estrutura do Repositório

### 1. **Background Removal**
- **Descrição:** Algoritmo para remoção automática de fundo de imagens monocromáticas. O fundo predominante é tornado transparente, gerando uma máscara (canal alpha) e uma imagem final sem o fundo.
- **Conteúdo:** 
  - Imagens de exemplo.
  - Código em Python.

### 2. **Barcode Area Finder**
- **Descrição:** Ferramenta para detectar e extrair a região de códigos de barras verticais. A técnica envolve operações de binarização, filtragem, dilatação e erosão para criar uma máscara da área do código de barras.
- **Conteúdo:** 
  - Imagens de exemplo.
  - Código em Python.

### 3. **Heart Finder**
- **Descrição:** Identificação de corações em imagens utilizando contornos e análise de componentes da Transformada Discreta de Fourier (DFT). Os primeiros e últimos 17 componentes são comparados com base no índice de correlação de Spearman para determinar se o contorno corresponde a um coração.
- **Conteúdo:** 
  - Imagens de exemplo.
  - Código em Python.

### 4. **Coloring Gray** *(Projeto Final - Em Desenvolvimento)* 
- **Descrição:** Rede neural convolucional residual, desenvolvida em PyTorch, para colorir imagens em escala de cinza, reconstruindo seus canais RGB. Este projeto utiliza aprendizado de máquina para gerar resultados realistas.
- **Conteúdo:**
  - Imagens de exemplo.
  - Código em Python.
  - Códigos em Python das últimas versões e variações testadas.

### 5. **resnet18_model_training.ipynb** *(Versão 3 do modelo em processo de treinamento)*
- **Descrição:** Notebook contendo a lógica implementada para definir e treinar o modelo de IA, desenvolvido em PyTorch, utilizado no projeto final **Coloring Gray**.

## Tecnologias Utilizadas
- Python
- OpenCV
- PyTorch
- Bibliotecas auxiliares: NumPy, Matplotlib, etc.

## Licença

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
