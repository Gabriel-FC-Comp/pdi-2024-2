/**
 * @file upload_form_control.js
 * @description Controla o upload de imagens, exibição prévia e envio para o servidor.
 */

// Seleciona os elementos do DOM
let fileInputButton = document.getElementById('btn_get_image_file');
let fileInput = document.getElementById('gray_image_file');
let fileNameLabel = document.getElementById('fileName');
let fileForm = document.getElementById('form_file');

/**
 * Cria uma imagem em branco com as mesmas dimensões da imagem original.
 * @param {number} width - Largura da imagem.
 * @param {number} height - Altura da imagem.
 * @returns {string} URL da imagem em branco gerada.
 */
function createWhiteImage(width, height) {
    let canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    let ctx = canvas.getContext('2d');
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = 'black';
    ctx.font = `${width / 2}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('...', width / 2, height / 2.6);
    return canvas.toDataURL();
}

/**
 * Atualiza o texto do label e exibe uma imagem temporária enquanto espera a resposta do servidor.
 */
function updateFileName() {
    if (fileInput.files.length > 0) {
        fileNameLabel.innerHTML = `Arquivo selecionado: ${fileInput.files[0].name}`;
        let fileUrl = URL.createObjectURL(fileInput.files[0]);
        let img = new Image();
        img.onload = function () {
            let whiteImageUrl = createWhiteImage(img.width, img.height);
            showImages(fileUrl, whiteImageUrl);
        };
        img.src = fileUrl;
    } else {
        fileNameLabel.innerHTML = 'Nenhum arquivo selecionado';
    }
}

/**
 * Envia a imagem para o servidor via POST e exibe a resposta.
 * @param {Event} event - Evento de envio do formulário.
 */
fileForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);
            alert('Imagem processada com sucesso!');
        } else if (data.error) {
            console.error(data.error);
            alert('Erro: ' + data.error);
        }
        if (data.file) {
            const imgBase64 = data.file;
            resultImage.src = 'data:image/png;base64,' + imgBase64;
            showImages(originalImage.src, resultImage.src);
        }
    })
    .catch(error => {
        console.error('Erro ao enviar o formulário:', error);
        alert('Ocorreu um erro ao enviar a imagem!');
    });
});

// Adiciona eventos ao input de arquivo e botão de upload
fileInput.addEventListener('change', updateFileName);
fileInputButton.addEventListener('click', () => fileInput.click());
