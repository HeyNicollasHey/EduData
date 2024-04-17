from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)

@app.route('/userregister', methods=['GET', 'POST'])
def redirecionar_cadastro_user():
    if request.method == 'GET':
        return render_template('userregister.html')
    elif request.method == 'POST':
        login = str(request.form.get('nome'))
        senha = str(request.form.get('senha'))

        if dao.inseriruser(login, senha, dao.conectardb()):
            return render_template('loginscreen.html')
        else:
            texto= 'e-mail já cadastrado'
            return render_template('userregister.html', msg=texto)

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))
    if (dao
            .verificarlogin(nome, senha, dao.conectardb())):
        return render_template('menu.html')
    else:
        return render_template('loginscreen.html')

@app.route('/pibxidhm', methods=['POST','GET'])
def gerarPibXIdhm():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados2()
    dados.drop(dados.sort_values(by=['PIB'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='IDHM', y='PIB', hover_data=['Municipios'])
    return render_template('pibxidhm.html', plot=fig.to_html())

@app.route('/idhmxfundamental', methods=['POST','GET'])
def gerarIdhmXFundamental():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados2()
    dados.drop(dados.sort_values(by=['Fundamental'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='IDHM', y='Fundamental', hover_data=['Municipios'])
    return render_template('idhmxfundamental.html', plot=fig.to_html())

@app.route('/idhmxmedio', methods=['POST','GET'])
def gerarIdhmXMedio():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados2()
    dados.drop(dados.sort_values(by=['Medio'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='IDHM', y='Medio', hover_data=['Municipios'])
    return render_template('idhmxmedio.html', plot=fig.to_html())

@app.route('/idhmxescolarizacao', methods=['POST','GET'])
def gerarIdhmXEscolarizacao():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados2()
    dados.drop(dados.sort_values(by=['Escolarizacao'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['IDHM'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='IDHM', y='Escolarizacao', hover_data=['Municipios'])
    return render_template('idhmxescolarizacao.html', plot=fig.to_html())

@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados2()
    fig2 = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig2.to_html())

@app.route('/melhoresedu')
def exibirmunicipiosedu():
    data = da.lerdados2()

    data['Melhor Escolarização'] = data['Escolarizacao']
    data.sort_values(by=['Melhor Escolarização'], ascending=False, inplace=True)
    fig = da.exibirgraficobarraseduc(data.head(70))

    return render_template('melhoresedu.html', plot=fig.to_html())

@app.route('/salvar_melhor_dado', methods=['POST'])
def salvar_melhor_dado():
    conexao = dao.conectardb()
    sucesso = dao.insert_correlacao(conexao, "Bom Jesus", "Escolarizacao", 99)
    if sucesso:
        return "Melhor dado salvo com sucesso!", 200
    else:
        return "Erro ao salvar o melhor dado.", 500

@app.route('/medioefundamental')
def exibirpopulacao():
    data = da.lerdados2()

    data['Alunos no Medio e Fundamental'] = data['Medio'] + data['Fundamental']
    data.sort_values(by=['Alunos no Medio e Fundamental'], ascending=False, inplace=True)
    fig = da.exibir_grafico_pizza(data.head(30))

    return render_template('medioefundamental.html', plot=fig.to_html())


@app.route('/correlacaoindicadores', methods=['GET', 'POST'])
def calcular_correlacao_individual():
    if request.method == 'GET':
        return render_template('escolherindicadores.html')
    else:
        ind1 = request.form.get('indicador1')
        ind2 = request.form.get('indicador2')
        dados, correlacao = da.correlacionar_indicadores(ind1, ind2)
        dados.columns = [ind1, ind2] #renomeado as colunas
        #normalizei os dados
        dados = (dados-dados.min())/(dados.max()-dados.min())
        fig = px.line(dados, x=dados.index, y=list(dados.columns))
        return render_template('correlacaoresultado.html', plot=fig.to_html(), valor=correlacao, ind1=ind1, ind2=ind2)

#        return f'<h1>{correlacao}</h1>'

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def firstscreen():
    return render_template('loginscreen.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)