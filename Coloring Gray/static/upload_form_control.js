let fileInputButton = document.getElementById('btn_get_image_file');
let fileInput = document.getElementById('gray_image_file');
let fileNameLabel = document.getElementById('fileName');

// Função para criar uma imagem em branco com as mesmas dimensões da imagem selecionada
function createWhiteImage(width, height) {
    // Criando um canvas com as dimensões da imagem
    let canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    
    // Obtendo o contexto do canvas para desenhar
    let ctx = canvas.getContext('2d');
    
    // Preenchendo o canvas com a cor branca
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
    
    // Adicionando o texto das reticências no centro do retângulo
    ctx.fillStyle = 'black';  // Cor do texto
    ctx.font = `${width / 2}px Arial`;  // Aumentei o tamanho da fonte para 60px (ajuste conforme necessário)
    ctx.textAlign = 'center';  // Alinha o texto no centro
    ctx.textBaseline = 'middle';  // Alinha o texto verticalmente no centro

    // Adicionando as reticências no centro
    ctx.fillText('...', width / 2, height/2.6);

    // Retornando a URL da imagem gerada
    return canvas.toDataURL();
}

// Atualiza o texto do label e exibe a imagem em branco enquanto espera a resposta do servidor
function updateFileName() {
    if (fileInput.files.length > 0) {
        fileNameLabel.innerHTML = `Arquivo selecionado: ${fileInput.files[0].name}`;

        // Criando uma URL temporária para o arquivo de imagem selecionado
        var fileUrl = URL.createObjectURL(fileInput.files[0]);

        // Carregar a imagem para pegar as dimensões
        let img = new Image();
        img.onload = function () {
            // Criar uma imagem em branco com as mesmas dimensões da imagem original
            var whiteImageUrl = createWhiteImage(img.width, img.height);

            // Exibir as imagens
            showImages(fileUrl, whiteImageUrl);  // Imagem em branco primeiro, depois a original após resposta
        };
        img.src = fileUrl;
    } else {
        fileNameLabel.innerHTML = 'Nenhum arquivo selecionado';
    }
}


// Adicionando eventos
fileInput.addEventListener('change', updateFileName);

// Quando o botão "Search Image" for clicado, dispara o clique no input[type="file"]
fileInputButton.addEventListener('click', () => {
    fileInput.click();
});

