import streamlit as st
import pandas as pd
import plotly_express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(layout='wide')

df = None  # Definindo inicialmente como None

try:
    df = pd.read_csv('gastosSenadores.csv')
except pd.errors.ParserError as e:
    print("Erro ao ler o arquivo CSV:", e)

if df is None:  # Se a leitura falhar, tente novamente com outro separador
    try:
        df = pd.read_csv('gastosSenadores.csv', sep=';')
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Erro ao ler o arquivo CSV:", e)
        
df.drop(columns=['DOCUMENTO', 'COD_DOCUMENTO'], inplace=True)

dfAgrupadoPorSenador = df.groupby('SENADOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
dfAgrupadoPorSenador = dfAgrupadoPorSenador.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()
dfAgrupadoPorSenador = dfAgrupadoPorSenador[:6]

senadorMaisGastou = dfAgrupadoPorSenador.loc[dfAgrupadoPorSenador['VALOR_REEMBOLSADO'].idxmax()]
gastosSenador = df[df['SENADOR'] == senadorMaisGastou['SENADOR']].reset_index()
gastosSenador.drop(columns=['index', 'CNPJ_CPF', 'MES'], inplace=True)

dfDespesaAgrupada = gastosSenador.groupby('TIPO_DESPESA')[['VALOR_REEMBOLSADO']].sum().sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()

dfAgrupadoPorSenador['VALOR_REEMBOLSADO'] = dfAgrupadoPorSenador['VALOR_REEMBOLSADO'].map(lambda x: locale.currency(x, grouping=True))

dfGastosAno = gastosSenador.groupby('ANO')[['VALOR_REEMBOLSADO']].sum().reset_index()

# dfAgrupadoFornecedor = df.groupby('FORNECEDOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor[1:7]
# # dfAgrupadoFornecedor['VALOR_REEMBOLSADO'] = dfAgrupadoFornecedor['VALOR_REEMBOLSADO'].map(lambda x: locale.currency(x, grouping=True))


senador = st.selectbox('Escolher Senador', options=[(i) for i in df['SENADOR'].unique()])


colInicial, colInicial2 = st.columns([10, 0.1])
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with colInicial:
    st.header(F'Gastos do Senador {locale.currency(dfGastosAno["VALOR_REEMBOLSADO"].sum(), grouping=True)}')
    with st.expander('Todos os gastos'):
        st.table(gastosSenador)
    with st.expander('Agrupado Por despesa'):
        st.table(dfDespesaAgrupada)
    
with col1:
    st.header('Gastos agrupados por ano')
    with st.expander('Tabelas dos gastos anuais'):
        st.table(dfGastosAno)

figLineGastosAno = px.line(dfGastosAno, x='ANO', y='VALOR_REEMBOLSADO')
col2.plotly_chart(figLineGastosAno, use_container_width=True)


