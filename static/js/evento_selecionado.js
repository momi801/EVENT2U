/*

Caminho para as imagens 
fetch("/api/imagem/1") // rota que devolve os dados da imagem
  .then(res => res.json())
  .then(dados => {
    document.getElementById("foto").src = dados.caminho; // ex: "uploads/img1.jpg"
  });

*/