# Importando bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date, timedelta

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
def carregar_dados(ticker, dt_inicial_api, dt_final_api):
    df = yf.Ticker(ticker).history(
        start=dt_inicial_api,
        end=dt_final_api + timedelta(days=1)
    )
    if df.empty:
        return pd.DataFrame(columns=['Data','Máximo','Mínimo','Fechamento','Volume'])
    
    df_tratado = df[['High','Low','Close','Volume']].copy()
    df_tratado.reset_index(inplace=True)
    df_tratado['Date'] = pd.to_datetime(df_tratado['Date'])
    
    if df_tratado['Date'].dt.tz is not None:
        df_tratado['Date'] = df_tratado['Date'].dt.tz_localize(None)

    df_tratado.columns = ['Data', 'Máximo', 'Mínimo', 'Fechamento', 'Volume']

    return df_tratado

# Definindo a função de previsão de dados
def prever_dados(df_tratado, periodo):
    if dados.shape[0] < 2:
        st.warning("Não há dados suficientes para gerar previsão.")
        st.stop()
    df_prophet = df_tratado.loc[:, ['Data', 'Fechamento']].copy()
    df_prophet = df_prophet.dropna()
    df_prophet.rename(columns={"Data": "ds", "Fechamento": "y"}, inplace=True)

    modelo = Prophet()
    modelo.fit(df_prophet)

    datas_futuras = modelo.make_future_dataframe(periods=int(periodo) * 30)
    previsoes = modelo.predict(datas_futuras)

    return modelo, previsoes

try:
    st.image('logo.jpeg', width=500)
except Exception:
    pass

with st.sidebar:
    st.header('Menu')
    empresa = st.selectbox("Selecione uma empresa:", list(tickers.keys()))
    ticker = tickers[empresa]
    st.write( f'Nome da ação: {ticker}')
    dt_inicial = st.date_input("Data inicial:", format="DD/MM/YYYY", value=date(2020, 1, 1))
    dt_final = st.date_input("Data final:", format="DD/MM/YYYY", value=date.today())
    meses = st.number_input("Meses de previsão", min_value=1, max_value=24, value=6)

if dt_inicial >= dt_final:
    st.warning("A data inicial deve ser anterior à data final.")
    st.stop()

dados = carregar_dados(ticker, dt_inicial, dt_final)

if dados.shape[0] != 0:

    st.header(f"Variação das ações - {empresa} ({ticker})")

    dados_tabela = dados.copy()

    dados_tabela['Data'] = dados_tabela['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(
        dados_tabela.style
        .set_properties(**{
            "text-align": "center"
        })
        .format({
        "Máximo": "R$ {:.2f}",
        "Mínimo": "R$ {:.2f}",
        "Fechamento": "R$ {:.2f}"
        })
    )
        

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

    fig = plot_plotly(modelo, previsoes, xlabel='Período', ylabel='Valor')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Nenhuma informação encontrada no período selecionado!")