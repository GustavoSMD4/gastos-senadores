import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
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
senadoresGastos = pd.DataFrame(st.session_state['senadoresGastos'])

senadorSelecionadoGastos = senadoresGastos[senadoresGastos['SENADOR'] == senadorSelecionado]

if senadorSelecionadoGastos is None:
    raise Exception('Não foram encontrados gastos para esse senador.')

if senadorDadosPessoais is None:
    st.warning('Não foi possível encontrar dados para o senador na API do governo.')
    
else:
    with st.container(border=True):
        st.header(F'Senador {senadorSelecionado}')
        col1, col2 = st.columns([1, 2.5])
        col1.image(senadorDadosPessoais['UrlFotoParlamentar'], width=200)  

        with col2:
            with st.container(border=False):
                
                st.metric('Nome Completo', senadorDadosPessoais['NomeCompletoParlamentar'])
                col3, col4 = st.columns(2)
                col3.metric('Partido', senadorDadosPessoais['SiglaPartidoParlamentar'])
                col4.metric('Estado', senadorDadosPessoais['UfParlamentar'])

    if len(senadorSelecionadoGastos) <= 0:
        st.warning('Não foram encontrado gastos para esse senador')
        
    else:
        
        senadorSelecionadoGastos['VALOR_REEMBOLSADO'] = senadorSelecionadoGastos['VALOR_REEMBOLSADO'].apply(lambda x: x.replace(',', ''))
        senadorSelecionadoGastos['VALOR_REEMBOLSADO'] = pd.to_numeric(senadorSelecionadoGastos['VALOR_REEMBOLSADO'])
        gastosAgrupadosAno = senadorSelecionadoGastos.groupby('ANO', as_index=False)[['VALOR_REEMBOLSADO']].sum()
        gastosAgrupadosAno['Valor'] = gastosAgrupadosAno['VALOR_REEMBOLSADO'].apply(lambda x: F"R${x:,.2f}")

        
        figLineGastosAno = px.line(gastosAgrupadosAno, x='ANO', y='VALOR_REEMBOLSADO',
                                   title='Gastos do Senador ao longo dos anos', text='Valor')
        
        figLineGastosAno.update_traces(textposition='top center')
        st.plotly_chart(figLineGastosAno, use_container_width=True)
        
        senadorSelecionadoGastosPorDespesa = senadorSelecionadoGastos.groupby('TIPO_DESPESA', as_index=False)[['VALOR_REEMBOLSADO']].sum()
        senadorSelecionadoGastosPorDespesa['Valor'] = senadorSelecionadoGastosPorDespesa['VALOR_REEMBOLSADO'].apply(lambda x: F"R${x:,.2f}")
        senadorSelecionadoGastosPorDespesa['Tipo'] = senadorSelecionadoGastosPorDespesa['TIPO_DESPESA'].str[0:10]
        
        figBarDespesas = px.bar(senadorSelecionadoGastosPorDespesa, x='Tipo', y='VALOR_REEMBOLSADO',
                                text='Valor', title='Gastos Agrupados por tipo de despesa')
        
        colGraph, colTable = st.columns(2)
        colGraph.plotly_chart(figBarDespesas, use_container_width=True)
        
        with colTable:
            ui.table(senadorSelecionadoGastosPorDespesa[['TIPO_DESPESA', 'Valor']])
        
        # st.dataframe(senadorSelecionadoGastos)


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



