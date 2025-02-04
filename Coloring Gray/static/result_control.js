let downloadButton = document.getElementById('btn_download');
let originalImage = document.getElementById('original_image');
let resultImage = document.getElementById('result_image');
let comparisonDiv = document.getElementById('div_comparison_images');

// Função para mostrar as imagens recebidas do servidor
function showImages(originalImageUrl, colorizedImageUrl) {
    originalImage.src = originalImageUrl;
    resultImage.src = colorizedImageUrl;
    comparisonDiv.style.display = 'flex';
    downloadButton.style.display = 'block';
}

// Função para baixar a imagem colorizada
function downloadImage() {
    let resultImage = document.getElementById('result_image');
    let a = document.createElement('a');
    a.href = resultImage.src;
    a.download = 'colorized_image.png'; // Nome do arquivo
    a.click();
}

downloadButton.addEventListener('click',downloadImage);