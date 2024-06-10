import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
import plotly_express as px
from buscarDados import getSenadores, getDadosPessoaisSenador, getGastosSenadores
from st_pages import Page, show_pages

def handleChangeSenador(senador):
    getDadosPessoaisSenador(senador)

st.set_page_config(layout='wide')

show_pages([
    Page('main.py', 'Senadores', '👨‍💼'),
    Page('partidos.py', 'Partidos', '🤝')
])

if 'senadores' not in st.session_state:
    getSenadores()
    
if 'senadorDadosPessoais' not in st.session_state:
    st.session_state['senadorDadosPessoais'] = None

if 'senadoresGastos' not in st.session_state:
    getGastosSenadores()
    
senadores: pd.DataFrame = st.session_state['senadores']

optionsEstado = ['TODOS'] + list(senadores['UfParlamentar'].unique())
optionsPartido = ['TODOS'] + list(senadores['SiglaPartidoParlamentar'].unique())
optionsSenadores = list(senadores['NomeParlamentar'].str.upper().unique())

estadoSenador = st.sidebar.selectbox('Estado', optionsEstado)

if estadoSenador != 'TODOS':
    partidosNoEstado = senadores[senadores['UfParlamentar'] == estadoSenador]
    optionsPartido = ['TODOS'] + list(partidosNoEstado['SiglaPartidoParlamentar'].unique())
    
    senadoresSelecionar = senadores[senadores['UfParlamentar'] == estadoSenador]
    
    optionsSenadores = senadoresSelecionar['NomeParlamentar'].str.upper()
    
partido = st.sidebar.selectbox('Partido', optionsPartido)

if partido != 'TODOS':
    
    if estadoSenador != 'TODOS':
        senadoresNoPartido = senadores[(senadores['SiglaPartidoParlamentar'] == partido)
                                        & (senadores['UfParlamentar'] == estadoSenador)]
        optionsSenadores = senadoresNoPartido['NomeParlamentar'].str.upper()
    else:
        senadoresNoPartido = senadores[senadores['SiglaPartidoParlamentar'] == partido]
        optionsSenadores = senadoresNoPartido['NomeParlamentar'].str.upper()
        

senadorSelecionado = st.sidebar.selectbox('Selecionar Senador', options=optionsSenadores)

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
        
        with st.expander('Despesas agrupadas por tipo.'):
            senadorDisplay = senadorSelecionadoGastosPorDespesa.sort_values('VALOR_REEMBOLSADO', ascending=False)
            ui.table(senadorDisplay[['TIPO_DESPESA', 'Valor']])


