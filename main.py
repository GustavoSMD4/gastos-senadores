import streamlit as st
import pandas as pd
import plotly_express as px
from buscarDados import getSenadores, getDadosPessoaisSenador, getGastosSenadores

def handleChangeSenador(senador):
    getDadosPessoaisSenador(senador)

st.set_page_config(layout='wide')

if 'senadores' not in st.session_state:
    getSenadores()
    
if 'senadorDadosPessoais' not in st.session_state:
    st.session_state['senadorDadosPessoais'] = None

if 'senadoresGastos' not in st.session_state:
    getGastosSenadores()
    
senadores: pd.DataFrame = st.session_state['senadores']

options = list(senadores['NomeParlamentar'].str.upper().unique())
senadorSelecionado = st.sidebar.selectbox('Selecionar Senador', options=options)

if senadorSelecionado != '':
    handleChangeSenador(senadorSelecionado)

senadorDadosPessoais: pd.DataFrame = st.session_state['senadorDadosPessoais']
senadoresGastos = pd.DataFrame = st.session_state['senadoresGastos']

dfGastosSenadores = senadoresGastos[senadoresGastos['SENADOR'] == senadorSelecionado]

st.header(F'Dados Senador {senadorSelecionado}')

if senadorDadosPessoais is None:
    st.warning('Não foi possível encontrar dados para o senador na API do governo.')
    
else: 
    col1, col2 = st.columns([1, 3])
    col1.image(senadorDadosPessoais['UrlFotoParlamentar'].iloc[0], width=200)  
    
    with col2:
        with st.container(border=False):
            col3, col4 = st.columns(2)
            with col3:
                st.info(F"Nome: {senadorDadosPessoais['NomeCompletoParlamentar'].iloc[0]}")
                st.info(F"Email: {senadorDadosPessoais['EmailParlamentar'].iloc[0]}")
            with col4:
                st.info(F"Partido: {senadorDadosPessoais['SiglaPartidoParlamentar'].iloc[0]}")
                st.info(F"Estado: {senadorDadosPessoais['UfParlamentar'].iloc[0]}")
            
    st.write(senadorDadosPessoais)
    
    st.dataframe(dfGastosSenadores)


# senadorDados = st.session_state['senadorDados']

# if senadorDados is not None:
#     st.table(senadorDados)
# else:
#     st.warning('Nenhum senador selecionado')


## app antigo        
# df.drop(columns=['DOCUMENTO', 'COD_DOCUMENTO'], inplace=True)

# dfAgrupadoPorSenador = df.groupby('SENADOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
# dfAgrupadoPorSenador = dfAgrupadoPorSenador.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()

# senadorMaisGastou = dfAgrupadoPorSenador.loc[dfAgrupadoPorSenador['VALOR_REEMBOLSADO'].idxmax()]

# dfAgrupadoFornecedor = df.groupby('FORNECEDOR')[['VALOR_REEMBOLSADO']].sum().reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor.sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()
# dfAgrupadoFornecedor = dfAgrupadoFornecedor[1:7]
# # dfAgrupadoFornecedor['VALOR_REEMBOLSADO'] = dfAgrupadoFornecedor['VALOR_REEMBOLSADO'].map(lambda x: locale.currency(x, grouping=True))

# senador = st.sidebar.selectbox('Escolher Senador', options=[(i) for i in dfAgrupadoPorSenador['SENADOR'].unique()])

# gastosSenador = df[df['SENADOR'] == senador].reset_index()
# gastosSenador.drop(columns=['index', 'CNPJ_CPF', 'MES'], inplace=True)

# dfDespesaAgrupada = gastosSenador.groupby('TIPO_DESPESA')[['VALOR_REEMBOLSADO']].sum().sort_values('VALOR_REEMBOLSADO', ascending=False).reset_index()

# dfGastosAno = gastosSenador.groupby('ANO')[['VALOR_REEMBOLSADO']].sum().reset_index()

# colInicial, colInicial2 = st.columns([10, 0.1])
# col1, col2 = st.columns([10, 0.1])
# col3, col4 = st.columns(2)

# with colInicial:
#     st.header(F'Gastos do Senador {senador}, total: {dfGastosAno["VALOR_REEMBOLSADO"].sum():,.2f}')
#     with st.expander('Todos os gastos'):
#         st.table(gastosSenador)
#     with st.expander('Agrupado Por despesa'):
#         st.table(dfDespesaAgrupada)
    
# with col1:
#     st.header('Gastos agrupados por ano')
#     with st.expander('Tabelas dos gastos anuais'):
#         st.table(dfGastosAno)
#     figLineGastosAno = px.line(dfGastosAno, x='ANO', y='VALOR_REEMBOLSADO')
#     st.plotly_chart(figLineGastosAno, use_container_width=True)



