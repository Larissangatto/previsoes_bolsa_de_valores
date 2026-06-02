# Importando bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date

# Configurações da página
st.set_page_config(
    page_title="Previsões da Bolsa",
    page_icon="📈",
    layout="wide"
)

# Título da página
st.title("Análise Preditiva")
st.markdown("""
### Valores das ações
""")

# Dicionário de tickers
tickers = {
    "Petrobras": "PETR4.SA",
    "Magazine Luiza": "MGLU3.SA",
    "Banco do Brasil": "BBAS3.SA",
    "Google": "GOOG",
    "Apple": "AAPL",
    "Microsoft": "MSFT"
}

# Definindo a função de carregar dados
@st.cache_data
def carregar_dados(ticker, dt_inicial, dt_final):
    df = yf.Ticker(ticker).history(
        start=dt_inicial.strftime('%Y-%m-%d'),
        end=dt_final.strftime('%Y-%m-%d')
    )

    df_tratado = df.loc[:, 'High':'Volume'].copy()
    df_tratado.index = df_tratado.index.strftime('%Y-%m-%d')
    df_tratado.reset_index(inplace=True)
    df_tratado.columns = ['Data', 'Máximo', 'Mínimo', 'Fechamento', 'Volume']

    return df_tratado

# Definindo a função de previsão de dados
def prever_dados(df_tratado, periodo):
    df_prophet = df_tratado.loc[:, ['Data', 'Fechamento']].copy()
    df_prophet.rename(columns={"Data": "ds", "Fechamento": "y"}, inplace=True)

    modelo = Prophet()
    modelo.fit(df_prophet)

    datas_futuras = modelo.make_future_dataframe(periods=int(periodo) * 30)
    previsoes = modelo.predict(datas_futuras)

    return modelo, previsoes

# Carregando imagem
st.image('logo.jpeg', width=400)

# Colocando um menu lateral
with st.sidebar:
    st.header('Menu')
    empresa = st.selectbox("Selecione uma empresa:", list(tickers.keys()))
    ticker = tickers[empresa]
    dt_inicial = st.date_input("Data inicial:", value=date(2020, 1, 1))
    dt_final = st.date_input("Data final:")
    meses = st.number_input("Meses de previsão", min_value=1, max_value=24, value=6)

if dt_inicial >= dt_final:
    st.warning("A data inicial deve ser anterior à data final.")
    st.stop()

# Carregando os dados
dados = carregar_dados(ticker, dt_inicial, dt_final)

# Condição para não ficar com a tabela e gráficos vazios
if dados.shape[0] != 0:

    st.header(f"Variação das ações - {empresa} ({ticker})")

    st.dataframe(dados)

    st.subheader("Variação no período")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados['Data'],
        y=dados['Fechamento'],
        name='Fechamento'
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.header(f"Previsão para os próximos {meses} meses")
    modelo, previsoes = prever_dados(dados, meses)
    fig = plot_plotly(modelo, previsoes, xlabel='Período', ylabel='Valor $')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Nenhuma informação encontrada no período selecionado!")