/**
 * @file result_control.js
 * @description Controla a exibição e o download das imagens recebidas do servidor.
 */

// Seleciona os elementos do DOM
let downloadButton = document.getElementById('btn_download');
let originalImage = document.getElementById('original_image');
let resultImage = document.getElementById('result_image');
let comparisonDiv = document.getElementById('div_comparison_images');

/**
 * Exibe as imagens recebidas do servidor.
 * @param {string} originalImageUrl - URL da imagem original.
 * @param {string} colorizedImageUrl - URL da imagem colorizada.
 */
function showImages(originalImageUrl, colorizedImageUrl) {
    originalImage.src = originalImageUrl;
    resultImage.src = colorizedImageUrl;
    comparisonDiv.style.display = 'flex';
    downloadButton.style.display = 'block';
}

/**
 * Baixa a imagem colorizada exibida na página.
 */
function downloadImage() {
    let a = document.createElement('a');
    a.href = resultImage.src;
    a.download = 'colorized_image.png'; // Nome do arquivo salvo
    a.click();
}

// Adiciona evento de clique para baixar a imagem
downloadButton.addEventListener('click', downloadImage);
