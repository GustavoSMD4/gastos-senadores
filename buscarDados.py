import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

url = 'https://gastosenadores.pythonanywhere.com'
 
def getSenadores():
    response = requests.get('https://legis.senado.leg.br/dadosabertos/senador/lista/atual')

    root = ET.fromstring(response.text)

    # Extract the data
    data = []
    for parlamentar in root.findall('.//Parlamentar'):
        identificacao = parlamentar.find('IdentificacaoParlamentar')
        mandato = parlamentar.find('Mandato')

        data.append({
            'NomeParlamentar': identificacao.find('NomeParlamentar').text,
            'NomeCompletoParlamentar': identificacao.find('NomeCompletoParlamentar').text,
            'UrlFotoParlamentar': identificacao.find('UrlFotoParlamentar').text,
            'FormaTratamento': identificacao.find('FormaTratamento').text,
            'SiglaPartidoParlamentar': identificacao.find('SiglaPartidoParlamentar').text,
            'UfParlamentar': identificacao.find('UfParlamentar').text,
            'DescricaoParticipacao': mandato.find('DescricaoParticipacao').text,
        })
        
    st.session_state['senadores'] = pd.DataFrame(data)
    
    return data
    
def getDadosPessoaisSenador(senador: str):
    senadores = st.session_state['senadores']
    senadorDados = senadores[senadores['NomeParlamentar'].str.upper() == senador]
    
    if len(senadorDados) <= 0:
        raise Exception('Dados não encontrados')
    
    # senadorDados = next((sen for sen in senadores if sen['NomeParlamentar'].upper() == senador))
    st.session_state['senadorDadosPessoais'] = senadorDados.iloc[0]
    
    return senadorDados
    
def getGastosSenadores():
    response = requests.get(url + '/senadores/gastos/')
    
    if response.status_code != 200:
        raise Exception(str(response.json().get('body')))
    
    senadoresGastos = response.json()
    st.session_state['senadoresGastos'] = senadoresGastos
    
    return senadoresGastos
    
