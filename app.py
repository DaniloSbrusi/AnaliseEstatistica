from flask import Flask, render_template, request, Response, send_file, url_for
from flask_bootstrap import Bootstrap5
import pandas as pd, matplotlib, matplotlib.pyplot as plt, requests, json, numpy as np, base64
from io import BytesIO

matplotlib.use('Agg')

app = Flask(__name__)
bootstrap = Bootstrap5(app)

df_populacao = pd.read_csv('static/populacao.csv')
df_frota = pd.read_csv('static/frota.csv')

df_populacao = df_populacao.loc[(df_populacao.ano>=2004)&(df_populacao.ano<=2020),['id_municipio', 'ano', 'populacao']]
df_frota = df_frota.loc[df_frota.mes==df_frota.mes.max(), ['id_municipio', 'ano', 'total']].rename(columns={'total': 'frota'})

df_estatistica = pd.merge(df_frota, df_populacao, on=['id_municipio','ano'])
df_estatistica['taxa'] = df_estatistica['frota'] / df_estatistica['populacao']

def get_id_municipios_uf(uf):
  url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      municipios_id_list = [municipio['id'] for municipio in data]
      return municipios_id_list
  else:
      raise ValueError('Erro ao fazer requisição: ' + response.status_code)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analise')
def analise():
    return render_template('analise.html')

@app.route('/estado')
def estado():
    return render_template('estado.html')

@app.route('/municipios')
def municipios():
    uf_list = get_uf()
    return render_template('municipio.html', uf_list=uf_list)

@app.route('/get-uf')
def get_uf():
  url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      lista_uf = [estado['sigla'] for estado in data]
      return sorted(lista_uf)
  else:
      raise ValueError('Erro ao fazer requisição: ' + response.status_code)

@app.route('/get-municipios/<uf>')
def get_municipios(uf):
  url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      municipios_name_list = [municipio['nome'] for municipio in data]
      municipios_id_list = [municipio['id'] for municipio in data]
      data = list(zip(municipios_name_list, municipios_id_list))
      return Response(json.dumps(data), mimetype='application/json')
  else:
      raise ValueError('Erro ao fazer requisição: ' + response.status_code)

@app.route('/populacao')
def get_populacao():
    id_municipio = int(request.args.get('id'))
    return df_populacao.loc[df_populacao.id_municipio == id_municipio] \
                       .drop('id_municipio', axis=1) \
                       .set_index('ano') \
                       .to_json(orient='columns')

@app.route('/frota')
def get_frota():
    id_municipio = int(request.args.get('id'))
    return df_frota.loc[df_frota.id_municipio == id_municipio] \
                   .drop('id_municipio', axis=1) \
                   .set_index('ano') \
                   .to_json(orient='columns')

    # df_estatistica.loc[df_estatistica.id_municipio == 1722081, ['ano', 'frota']].set_index('ano').to_json(orient='columns')

@app.route('/taxa')
def taxa():
    ano = int(request.args.get('ano'))
    print(ano)
    return df_estatistica.loc[df_estatistica.ano == ano].taxa.to_json(orient='records')

@app.route('/taxa-municipio')
def taxa_municipio():
    id_municipio = int(request.args.get('id'))
    return df_estatistica.loc[df_estatistica.id_municipio == id_municipio, ['ano', 'taxa']].set_index('ano').to_json()

@app.route('/histograma', methods=['POST'])
def exibir_histograma():

    estado = request.form.get('estado')
    ano = int(request.form.get('ano'))

    df_estado = df_estatistica[df_estatistica.id_municipio.isin(get_id_municipios_uf(estado))]
    dados = df_estado.loc[df_estado.ano == ano].taxa

    plt.figure()
    plt.hist(dados)

    mean = np.mean(dados)
    std = np.std(dados)

    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)

    for i in [-2,-1,1,2]:
        plt.axvline(mean+i*std, color='gray', linestyle='dashed', linewidth=1)

    plt.title(f'Taxa de veículos por habitante em {estado} no ano de {ano}')
    plt.xlabel('Taxa')
    plt.ylabel('Frequência')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    return Response(img_buffer.getvalue(), mimetype='image/png')

@app.route('/gerar_grafico', methods=['POST'])
def gerar_grafico():

    ano = int(request.form.get('ano'))
    pop_min = int(request.form.get('min'))
    pop_max = int(request.form.get('max'))

    dados = df_estatistica.loc[(df_estatistica.ano == ano) & (df_estatistica.populacao >= pop_min) & (df_estatistica.populacao <= pop_max)].taxa
    
    plt.figure()
    plt.hist(dados)

    mean = np.mean(dados)
    std = np.std(dados)
    var = np.var(dados)
    qtd_2std = len(dados[(dados>mean-2*std)&(dados<mean+2*std)]) / len(dados)
    qtd_1std = len(dados[(dados>mean-std)&(dados<mean+std)]) / len(dados)

    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1)

    for i in [-2,-1,1,2]:
        plt.axvline(mean+i*std, color='gray', linestyle='dashed', linewidth=1)

    plt.title(f'Taxa de veículos por habitante')
    plt.xlabel('Taxa')
    plt.ylabel('Frequência')

    # salvar o gráfico em um arquivo PNG
    png_output = BytesIO()
    plt.savefig(png_output, format='png')
    png_output.seek(0)

    # criar o dicionário com as informações a serem retornadas
    data = {
        'mean': round(mean, 4),
        'std': round(std, 4),
        'var': round(var, 4),
        'qtd_2std': str(round(qtd_2std*100, 2)) + '%',
        'qtd_1std': str(round(qtd_1std*100, 2)) + '%',
        'grafico': base64.b64encode(png_output.getvalue()).decode('utf-8')
    }

    # retornar o dicionário como uma resposta JSON

    return json.dumps(data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)


# municipios com mais de 10 mil habitantes
# df_estatistica.loc[(df_estatistica.ano == 2020) & (df_estatistica.populacao >= 10000)].id_municipio

# dados dos municipios grandes
# df_estatistica[df_estatistica.id_municipio.isin(municipios_grandes)]