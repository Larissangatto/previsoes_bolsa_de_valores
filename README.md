# 📈 Previsões da Bolsa de Valores

### 💻🤖 Aplicação web para previsão de ações nas bolsas de valores utilizando Machine Learning

Projeto é uma **aplicação web interativa** que utiliza **Machine Learning** para fazer previsões de preços de ações na bolsa de valores.


## Preview

Acesse o projeto publicado / Access the deployed project:
[ https://previsoesbolsadevalores.streamlit.app/]


## 🚀 Tecnologias Utilizadas / Technologies Used

  - Python
  - Streamlit (framework web)
  - Pandas & NumPy (manipulação de dados)
  - Scikit-learn (modelo de Machine Learning)
  - yfinance / Yahoo Finance (dados reais da bolsa)


## 📂 Estrutura do Projeto / Project Structure
```text
previsoes_bolsa_de_valores/
├── app.py              # Aplicação Python
├── logo.jpeg           # Logo do projeto
├── requirements.txt    # Dependências
└── README.md          # Documentação 
```


## 🛠️ Como Executar

1. **Clone o repositório**
```bash
git clone https://github.com/Larissangatto/previsoes_bolsa_de_valores.git
cd previsoes_bolsa_de_valores
```
2. **Instale as dependências**
```bash
pip install -r requirements.txt
```
3. **Execute a aplicação**
```bash
streamlit run app.py 
```

## 📖 Funcionalidades
### No menu lateral:
- Selecionar empresa para previsão
- Escolher data inicial e final (base para o modelo)
- Definir quantidade de meses para previsão
  
### O programa apresenta:
- 📊 Tabela com os dados históricos utilizados
- 📈 Gráfico da variação real no período analisado
- 🔮 Gráfico com as previsões geradas
- 📉 Faixa de confiança/erro das previsões
  
### Como funciona:
1. O usuário seleciona uma empresa (ex: PETR4, VALE3)
2. Escolhe um período de dados históricos (data inicial e final)
3. Define quantos meses quer prever no futuro
4. O sistema busca dados reais da bolsa e treina um modelo de ML
5. Exibe gráficos mostrando:
   - Histórico real dos preços
   - Previsões futuras
   - Faixa de erro estimada

## ⚠️ **AVISO IMPORTANTE**

### 🚨 Este projeto é **EXCLUSIVAMENTE EDUCACIONAL**
- Não deve ser utilizado como ferramenta de consulta para decisões de investimento reais
- As previsões geradas são **simulações** baseadas em modelos estatísticos simples
- O mercado financeiro é influenciado por inúmeras variáveis imprevisíveis (política, economia global, notícias, etc.)
- **Nenhuma previsão aqui gerada deve ser interpretada como recomendação de compra, venda ou manutenção de ativos**
- Invista com responsabilidade e sempre consulte profissionais capacitados

### 🔒 Isenção de responsabilidade
Os autores deste projeto não se responsabilizam por quaisquer perdas financeiras, danos ou prejuízos resultantes do uso das informações ou previsões geradas por esta aplicação. O código é fornecido "como está" apenas para fins de aprendizado.