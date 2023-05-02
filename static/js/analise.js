$(document).ready(function() {
  $('form').submit(function(event) {
    event.preventDefault();
    var inputMin = $('#min');
    var inputMax = $('#max');
    if (inputMin.val() === inputMax.val()) {
      alert('Os valores de população selecionados devem ser diferentes.');
    } else if (parseInt(inputMin.val()) > parseInt(inputMax.val())) {
      alert('A população mínima é maior que a população máxima, por favor verifique.');
    } else if (parseInt(inputMax.val()) < parseInt(inputMin.val())) {
      alert('A população máxima é menor que a população mínima, por favor verifique.');
    } else {
      var formData = new FormData(this);
      $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
          var content = $('#result');
          content.removeAttr('hidden');
          var img = $('#grafico');
          img.attr('src', 'data:image/png;base64,' + data.grafico);
          var mean = $('#mean');
          var std = $('#std');
          var variancia = $('#var');
          var qtd1std = $('#qtd-1');
          var qtd2std = $('#qtd-2');
          mean.text(data.mean);
          std.text(data.std);
          variancia.text(data.var);
          qtd1std.text(data.qtd_1std);
          qtd2std.text(data.qtd_2std);
        },
        error: function(xhr, status, error) {
          alert('Ocorreu um erro ao gerar o histograma.');
        }
      });
      return false;
    }
  });
});
