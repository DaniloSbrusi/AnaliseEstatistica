function preencherMunicipios() {
  const uf_selected = $('#uf-select')[0].value;
  console.log(uf_selected);
  $.ajax({
    url: '/get-municipios/' + uf_selected,
    method: 'GET',
    success: function (response) {

      var select_municipios = $('#municipios-select');
      select_municipios.removeAttr('disabled');
      select_municipios.empty();
      select_municipios.append($('<option>').text('Selecione uma opção').attr('disabled', true).attr('selected', true));

      $.each(response, function (index, value) {
        select_municipios.append($('<option>').text(value[0]).val(value[1]));
      });
    },
    error: function (xhr, status, error) {
      console.log('Error:', error);
    }
  });
}

function renderizar_grafico() {
  var chart_populacao = echarts.init(document.getElementById('chart-populacao'));
  chart_populacao.showLoading();
  $.ajax({
    url: '/populacao',
    type: "GET",
    data: ({ 'id': $('#municipios-select option:selected')[0].value }),
    // data: ({'ano': 2020}),
    dataType: "json",
    success: function (data) {
      console.log(data);
      chart_populacao.setOption({
        title: {
          left: 'center',
          text: 'População de ' + $('#municipios-select option:selected').text()
        },
        xAxis: {
          type: 'category',
          data: Object.keys(data.populacao)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: function (value, index) {
              return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
            }
          },
          scale: true
        },
        series: [{
          data: Object.values(data.populacao),
          type: 'line'
        }],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c} habitantes'
        },
        dataZoom: {
          type: 'slider'
        }
      });
      chart_populacao.hideLoading();
    }
  });

  var chart_frota = echarts.init(document.getElementById('chart-frota'));
  chart_frota.showLoading();
  $.ajax({
    url: '/frota',
    type: "GET",
    data: ({ 'id': $('#municipios-select option:selected')[0].value }),
    dataType: "json",
    success: function (data) {
      console.log(data);
      chart_frota.setOption({
        title: {
          left: 'center',
          text: 'Frota de ' + $('#municipios-select option:selected').text()
        },
        xAxis: {
          type: 'category',
          data: Object.keys(data.frota)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: function (value, index) {
              return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
            }
          },
          scale: true
        },
        series: [{
          data: Object.values(data.frota),
          type: 'line'
        }],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c} veículos'
        },
        dataZoom: {
          type: 'slider'
        }
      });
      chart_frota.hideLoading();
    }
  });

  var chart_taxa = echarts.init(document.getElementById('chart-taxa'));
  chart_taxa.showLoading();
  $.ajax({
    url: '/taxa-municipio',
    type: "GET",
    data: ({ 'id': $('#municipios-select option:selected')[0].value }),
    dataType: "json",
    success: function (data) {
      console.log(data);
      chart_taxa.setOption({
        title: {
          left: 'center',
          text: 'Taxa de veículos por habitante em ' + $('#municipios-select option:selected').text()
        },
        xAxis: {
          type: 'category',
          data: Object.keys(data.taxa)
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: function (value, index) {
              return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
            }
          },
          scale: true
        },
        series: [{
          data: Object.values(data.taxa),
          type: 'line'
        }],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c} veículos por habitante'
        },
        dataZoom: {
          type: 'slider'
        }
      });
      chart_taxa.hideLoading();
    }
  });
}


