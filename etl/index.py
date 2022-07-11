import requests
import pandas as pd
import numpy as np
import sqlite3
import src.constants.querys as querys
from src.utils.handleQueryExecute import handleQueryExecute


connect = sqlite3.connect('../database/data.db')

data_result = []
df_cleaned = pd.DataFrame()
df_nomes_existentes = pd.DataFrame()
df_pais_existente = pd.DataFrame()


def populateDataFramesIds(rowId, userName, countryName):
    global df_nomes_existentes, df_pais_existente, df_cleaned

    # Verifica se já existe o nome na base:
    # Se sim reutiliza o id existente, se não cria um id e adiciona o nome ao dataframe.
    if userName in df_nomes_existentes['nome'].unique():
        if df_cleaned.loc[[rowId], 'id_nome'].isnull().values.any():
            existing_id = df_nomes_existentes.loc[df_nomes_existentes.nome == userName, 'id'].values[0]

            # Altera o id_nome de todos os nomes iguais ao nome recebido.
            df_cleaned.loc[df_cleaned.nome == userName, 'id_nome'] = existing_id
    else:
        new_id = len(df_nomes_existentes) + 1

        df_newLine =  pd.DataFrame.from_records([{'nome': userName, 'id': new_id}])
        df_nomes_existentes = pd.concat([df_nomes_existentes, df_newLine], ignore_index=True)

        # Altera o id_nome de todos os nomes iguais ao nome recebido.
        df_cleaned.loc[df_cleaned.nome == userName, 'id_nome'] = new_id

    # Verifica se já existe o pais na base:
    # Se sim reutiliza o id existente, se não cria um id e adiciona o pais ao dataframe.
    if countryName in df_pais_existente['nome'].unique():
        if df_cleaned.loc[[rowId], 'id_pais'].isnull().values.any():
            existing_id = df_pais_existente.loc[df_pais_existente.nome == countryName, 'id'].values[0]

            # Altera o id_pais de todos os paises iguais ao pais recebido.
            df_cleaned.loc[df_cleaned.pais == countryName, 'id_pais'] = existing_id
    else:
        new_id = len(df_pais_existente) + 1

        df_newLine = pd.DataFrame.from_records([{'nome': countryName, 'id': new_id}])
        df_pais_existente = pd.concat([df_pais_existente, df_newLine], ignore_index=True)

        # Altera o id_pais de todos os paises iguais ao pais recebido.
        df_cleaned.loc[df_cleaned.pais == countryName, 'id_pais'] = new_id


def extract_data(loops):
    print('[EXTRAÇÃO INICIADA]')
    result = []

    for i in range(loops):
        request = requests.get("https://randomuser.me/api/?results=50")
        result = result + request.json()['results']

    print('[EXTRAÇÃO FINALIZADA]')
    return result


def transform_data(data):
    print('[TRANSFORMAÇÃO INICIADA]')

    global df_nomes_existentes, df_pais_existente, df_cleaned

    df_cleaned = pd.json_normalize(data, sep='_')

    df_cleaned = df_cleaned.rename(
        columns={'gender': 'genero', 'name_first': 'nome', 'dob_age': 'idade', 'location_country': 'pais'})

    df_cleaned = df_cleaned[['genero', 'nome', 'idade', 'pais']]

    df_cleaned[['id_nome', 'id_pais']] = np.nan  # create column valor nan

    df_nomes_existentes = pd.read_sql_query(querys.getDimNames, connect)
    df_pais_existente = pd.read_sql_query(querys.getDimPais, connect)

    df_cleaned.apply(lambda row: populateDataFramesIds(row.name, row.nome, row.pais), axis=1)

    df_cleaned = df_cleaned[['genero', 'idade', 'id_nome', 'id_pais']]
    print('[TRANSFORMAÇÃO FINALIZADA]')


def loading_data():
    print('[LOADING INICIADO]')

    df_nomes_existentes.to_sql(name='dim_nomes', if_exists='replace', con=connect, index=False)
    df_pais_existente.to_sql(name='dim_paises', if_exists='replace', con=connect, index=False)
    df_cleaned.to_sql(name='dim_usuarios', if_exists='append', con=connect, index=False)

    handleQueryExecute(connect, querys.cleanFato)
    handleQueryExecute(connect, querys.insertIntoFato)

    print('[LOADING FINALIZADO]')


if __name__ == '__main__':
    print('-' * 30)
    print('[PROGRAMA INICIADO] \n')

    data_result = extract_data(50)
    transform_data(data_result)
    loading_data()

    connect.close()

    print('\n[PROGRAMA FINALIZADO]')
    print('-' * 30)
