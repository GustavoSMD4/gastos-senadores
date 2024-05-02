import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(layout='wide')

df = None

try:
    df = pd.read_csv('gastosSenadores.csv')
except pd.errors.ParserError as e:
    print("Erro ao ler o arquivo CSV:", e)

if df is None:
    try:
        df = pd.read_csv('gastosSenadores.csv', sep=';')
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Erro ao ler o arquivo CSV:", e)
        
df.drop(columns=['DOCUMENTO', 'COD_DOCUMENTO'], inplace=True)

dfAgrupadoPorSenador = df.groupby('SENADOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
dfAgrupadoPorSenador = dfAgrupadoPorSenador.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()

# senadorMaisGastou = dfAgrupadoPorSenador.loc[dfAgrupadoPorSenador['VALOR_REEMBOLSADO'].idxmax()]

# dfAgrupadoFornecedor = df.groupby('FORNECEDOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor[1:7]
# # dfAgrupadoFornecedor['VALOR_REEMBOLSADO'] = dfAgrupadoFornecedor['VALOR_REEMBOLSADO'].map(lambda x: locale.currency(x, grouping=True))

senador = st.sidebar.selectbox('Escolher Senador', options=[(i) for i in dfAgrupadoPorSenador['SENADOR'].unique()])

gastosSenador = df[df['SENADOR'] == senador].reset_index()
gastosSenador.drop(columns=['index', 'CNPJ_CPF', 'MES'], inplace=True)

dfDespesaAgrupada = gastosSenador.groupby('TIPO_DESPESA')[['VALOR_REEMBOLSADO']].sum().sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()

dfGastosAno = gastosSenador.groupby('ANO')[['VALOR_REEMBOLSADO']].sum().reset_index()

colInicial, colInicial2 = st.columns([10, 0.1])
col1, col2 = st.columns([10, 0.1])
col3, col4 = st.columns(2)

with colInicial:
    st.header(F'Gastos do Senador {senador}, total: {dfGastosAno["VALOR_REEMBOLSADO"].sum():,.2f}')
    with st.expander('Todos os gastos'):
        st.table(gastosSenador)
    with st.expander('Agrupado Por despesa'):
        st.table(dfDespesaAgrupada)
    
with col1:
    st.header('Gastos agrupados por ano')
    with st.expander('Tabelas dos gastos anuais'):
        st.table(dfGastosAno)
    figLineGastosAno = px.line(dfGastosAno, x='ANO', y='VALOR_REEMBOLSADO')
    st.plotly_chart(figLineGastosAno, use_container_width=True)



