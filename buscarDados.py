import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

url = 'http://127.0.0.1:5000'
 
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
            'EmailParlamentar': identificacao.find('EmailParlamentar').text,
            'NumeroTelefone': identificacao.find('.//Telefone/NumeroTelefone').text,
            'SiglaPartidoParlamentar': identificacao.find('SiglaPartidoParlamentar').text,
            'UfParlamentar': identificacao.find('UfParlamentar').text,
            'DescricaoParticipacao': mandato.find('DescricaoParticipacao').text,
        })
        
    st.session_state['senadores'] = pd.DataFrame(data)
    
    return data
    
def getDadosPessoaisSenador(senador: str):
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
            'EmailParlamentar': identificacao.find('EmailParlamentar').text,
            'NumeroTelefone': identificacao.find('.//Telefone/NumeroTelefone').text,
            'SiglaPartidoParlamentar': identificacao.find('SiglaPartidoParlamentar').text,
            'UfParlamentar': identificacao.find('UfParlamentar').text,
            'DescricaoParticipacao': mandato.find('DescricaoParticipacao').text,
        })

    data = pd.DataFrame(data)
    senadorReturn = data[data['NomeParlamentar'].str.upper() == senador.upper()]
    st.session_state['senadorDadosPessoais'] = senadorReturn
    
    return senador
    
def getGastosSenadores():
    response = requests.get(url + '/senadores/gastos/')
    
    if response.status_code != 200:
        raise Exception(response.json().get('body'))
    
    senadoresGastos = response.json()
    st.session_state['senadoresGastos'] = pd.DataFrame(senadoresGastos)
    
    return senadoresGastos
    