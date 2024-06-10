import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui

senadores: pd.DataFrame = st.session_state['senadores']
senadoresGastos: pd.DataFrame = st.session_state['senadoresGastos']

listaPartidos = senadores['SiglaPartidoParlamentar'].unique()

qtdeParlamentarPartido = senadores.copy()
qtdeParlamentarPartido = senadores.groupby('SiglaPartidoParlamentar', as_index=False)[['NomeParlamentar']].count()
qtdeParlamentarPartido.rename(columns={'NomeParlamentar': 'Qtde no partido'}, inplace=True)
qtdeParlamentarPartido.sort_values('Qtde no partido', inplace=True, ascending=False)

with st.expander('Lista de partidos e qtde de parlamentares'):
    ui.table(qtdeParlamentarPartido)

options = qtdeParlamentarPartido['SiglaPartidoParlamentar']
partidoSelecionado = st.sidebar.selectbox('Partido', options=options)

gastosSenadores = senadoresGastos.copy()

