# Importando bibliotecas
import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date
# Título da página
st.title("Análise Preditiva")
st.markdown("""
            ### Valores das ações 
            """)
# listagem de tickers
listagem =["PETR4.SA",
           "MGLU3.SA",
           "BBAS3.SA",
           "GOOG",
           "AAPL",
           "MSFT"]  
 # dicionario de tickers
tickers = {"PETR4.SA": "Petrobras",
           "MGLU3.SA": "Magazine Luiza",
           "BBAS3.SA": "Banco do Brasil",
           "GOOG": "Google",
           "AAPL": "Apple",
           "MSFT": "Microsoft"
           }
# Definindo a função de carregar dados
def carregar_dados(ticker,dt_inicial,dt_final):
    df=yf.Ticker(ticker).history(start=dt_inicial.strftime("%Y-%m-%d"),
                                 end=dt_final.strftime("%Y-%m-%d"))
    df_tratado = df.loc[:, 'High':'Volume'].copy()
    df_tratado.index = df_tratado.index.strftime('%Y-%m-%d')
    df_tratado.reset_index(inplace=True)
    df_tratado.columns = ['Data','Máximo', 'Mínimo', 'Fechamento', 'Volume']
          
    return df_tratado

# Defininado a função de previsão de dados
def prever_dados(df_tratado,periodo):
    df_tratado = df_tratado.loc[:,['Data','Fechamento']] 
    df_tratado.rename(columns={"Data":"ds","Fechamento":"y"},inplace=True)
    
    modelo = Prophet()
    modelo.fit(df_tratado)
    
    datas_futuras = modelo.make_future_dataframe(periods= int(periodo)*30)
    previsoes = modelo.predict(datas_futuras)
    
    return modelo, previsoes
          
        
#Carregando imagem
st.image('logo.jpeg',width=400)
# colocando um menu lateral
with st.sidebar:
    st.header('Menu')
    ticker = st.selectbox("Selecione uma ação:",listagem)
    dt_inicial = st.date_input("Data inicial:", value=date(2020,1,1))
    dt_final = st.date_input("Data final:")
    meses = st.number_input("Meses de previsão",min_value=1,max_value=24,value=6)

# carregando os dados
dados = carregar_dados(ticker,dt_inicial,dt_final)
 # condição para não ficar com a tabela e gráficos vázios
if dados.shape[0]!=0:

    st.header(f"Variação das ações {tickers[ticker]}")

    st.dataframe(dados)

    st.subheader("Variação no período")
    fig = go.Figure()
    fig.add_trace(go.Scatter (x=dados['Data'] , y=dados['Fechamento'], name='fechamento'))
    st.plotly_chart(fig)
    
    st.header (f"Previsão para os próximos {meses} meses")
    modelo, previsoes = prever_dados(dados, meses)
    fig = plot_plotly(modelo,previsoes,xlabel ='Período',ylabel='Valor $') 
    st.plotly_chart(fig)
else:
    st.warning("Nenhuma informação encotrada no perído selecionado!")

