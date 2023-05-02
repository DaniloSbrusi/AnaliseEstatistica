function gerarGrafico() {
  var estado = $('#estado').val();
  var ano = $('#ano').val();
  
  var form = document.querySelector('form');
  var formData = new FormData(form);

  $.ajax({
    url: '/histograma',
    type: 'POST',
    // data: {estado: estado, ano: ano},
    data: formData,
    success: function(data) {
      var url = URL.createObjectURL(new Blob([data], {type: 'image/png'}));
      $('#imagem-grafico').attr('src', url);
    },
    error: function(xhr, status, error) {
      alert('Erro ao gerar gráfico: ' + error);
    }
  });
}