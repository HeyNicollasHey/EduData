import pandas as pd
import plotly.express as px

def lerdados():
    dados = pd.read_csv('IBGEeducacao.csv')
    dados.drop(columns=['Municipios'], inplace=True)
    return dados

def lerdados2():
    dados = pd.read_csv('IBGEeducacao.csv')
    return dados

def exibirmapacorrelacoes(data):
    data.drop(columns=['Municipios'], inplace=True)
    fig = px.imshow(data.corr())
    return fig

def exibirgraficobarraseduc(dados):
    fig = px.bar(dados, x='Melhor Escolarização', y='Municipios')
    return fig

def exibir_grafico_pizza(data):
    fig = px.pie(data, values='Alunos no Medio e Fundamental', names='Municipios', title="Cidades com Maior Número de Alunos no Ensino Médio e Fundamental")
    fig.update_layout(
        width=800,
        height=600
    )
    return fig