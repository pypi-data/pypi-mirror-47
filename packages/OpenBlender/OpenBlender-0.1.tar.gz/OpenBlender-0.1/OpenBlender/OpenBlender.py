# Copyright (c) 2019 OpenBlender.io
# Simplicity is key.


from urllib.request import Request, urlopen
from urllib.request import urlopen
from urllib.parse import urlencode
from contextlib import closing
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import time
import math
import json

url = 'http://52.8.156.139/oro/'

def call(action, json_parametros):
    try:
        respuesta = ''
        if 'test_call' in json_parametros and json_parametros['test_call'] == 1:
            print('test')
            global url
            url = 'https://bronce-federicorgs.c9users.io/'
        if action == 'API_createDataset':
            respuesta = API_createDataset(json_parametros)
        elif action == 'API_insertObservationsFromDataFrame':
            respuesta = API_insertObservationsFromDataFrame(json_parametros)
        elif action == 'API_getObservationsFromDataset':
            respuesta = API_getSampleObservationsFromDataset(json_parametros)
        elif action == 'API_powerModel':
            respuesta = API_powerModel(json_parametros)
        else:
            data = urlencode({'action' : action, 'json' : json.dumps(json_parametros)}).encode()
            with closing(urlopen(url, data)) as response:
                return json.loads(response.read().decode())
        return respuesta
    except Exception as e:
        print(json.dumps({"status": "internal error", "msg": str(e)}))
        return json.dumps({"status": "internal error", "msg": str(e)})
    
def API_createDataset(json_parametros):
    action = 'API_createDataset'
    df, valido_df, msj = comprobarJSONaDF(json_parametros['dataframe'])
    if not valido_df:
        return msj
    n_filas = df.shape[0]
    tam_pedazo_ini = 1000
    insert_observations = True
    json_particion = json_parametros.copy()
    if 'insert_observations' in json_parametros:
        insert_observations = json_parametros['insert_observations'] == 1
    test_output = False
    if 'test_output' in json_parametros:
        test_output = json_parametros['test_output'] == 1
    respuesta0 = None
    
    # Primer pedazo para crear el dataset
    if not test_output and n_filas > tam_pedazo_ini:
        if insert_observations:
            start = time.time()
            tam_pedazo_ini = tam_pedazo_ini if n_filas > tam_pedazo_ini else n_filas
            json_particion['dataframe'] = df.sample(n=tam_pedazo_ini).to_json()
            json_particion_molde = json_particion.copy()
            json_particion_molde['insert_observations'] = 0
            data = urlencode({'action' : action, 'json' : json.dumps(json_particion_molde)}).encode()
            with closing(urlopen(url, data)) as response:
                respuesta = response.read().decode()
            #print(respuesta)
            respuesta0 = respuesta
            json_particion['id_dataset'] = json.loads(respuesta)['id_dataset']
            print("Dataset created succesfully, id: " + str(json_particion['id_dataset']))
            print("Uploading..")
            stop = time.time()
            segundos = stop - start
            tam_pedazo = int(round(tam_pedazo_ini * 30 / segundos))
            
            action = 'API_insertObservationsFromDataFrame'
            for i in range(0, n_filas, tam_pedazo):
                json_particion['dataframe'] = df[i:i+tam_pedazo].to_json()
                data = urlencode({'action' : action, 'json' : json.dumps(json_particion)}).encode()
                with closing(urlopen(url, data)) as response:
                    respuesta = response.read().decode()
                # Imprimir avance
                avance = round((i + tam_pedazo) / n_filas * 100, 3)
                if avance > 100:
                    print('100% completed..')
                    print("Finishing..")
                else:
                    print(str(avance) + "% completed.")
                    print("Uploading...")
        else:
            json_particion['dataframe'] = df[0:tam_pedazo_ini].to_json()
            data = urlencode({'action' : action, 'json' : json.dumps(json_particion)}).encode()
            with closing(urlopen(url, data)) as response:
                return json.loads(response.read().decode())
    else:
        tam_pedazo_ini = tam_pedazo_ini if n_filas > tam_pedazo_ini else n_filas
        json_particion['dataframe'] = df.sample(n=tam_pedazo_ini).to_json()
        data = urlencode({'action' : action, 'json' : json.dumps(json_particion)}).encode()
        with closing(urlopen(url, data)) as response:
            return json.loads(response.read().decode())
    return respuesta0

def API_insertObservationsFromDataFrame(json_parametros):
    action = 'API_insertObservationsFromDataFrame'
    df, valido_df, msj = comprobarJSONaDF(json_parametros['dataframe'])
    if not valido_df:
        return msj
    n_filas = df.shape[0]
    n_columnas = df.shape[1]
    tam_pedazo_ini = 100
    json_particion = json_parametros.copy()
    if n_filas > tam_pedazo_ini:
        # Inserta por primera vez para medir tiempos.
        start = time.time()
        json_particion['dataframe'] = df[0:tam_pedazo_ini].to_json()
        data = urlencode({'action' : action, 'json' : json.dumps(json_particion)}).encode()
        with closing(urlopen(url, data)) as response:
            respuesta = response.read().decode()
        respuesta0 = respuesta
        stop = time.time()
        segundos = stop - start
        tam_pedazo = int(round(tam_pedazo_ini * 30 / segundos))
        print("Uploading..")
        json_particion = json_parametros.copy()
        for i in range(tam_pedazo_ini, n_filas, tam_pedazo):
            json_particion['dataframe'] = df[i:i+tam_pedazo].to_json()
            data = urlencode({'action' : action, 'json' : json.dumps(json_particion)}).encode()
            with closing(urlopen(url, data)) as response:
                respuesta = response.read().decode()
            # Imprimir avance
            avance = round((i + tam_pedazo)/n_filas * 100, 3)
            if avance > 100:
                print('100% completed..')
                print("Finished.")
            else:
                print(str(avance) + "% completed.")
                print("Uploading...")
                time.sleep(2)
    else:
        data = urlencode({'action' : action, 'json' : json.dumps(json_parametros)}).encode()
        with closing(urlopen(url, data)) as response:
            return json.loads(response.read().decode())
    return respuesta


def API_getSampleObservationsFromDataset(json_parametros):
    action = 'API_getSampleObservationsFromDataset'
    
    start = time.time()
    json_parametros['tamano_bin'] = 50
    json_parametros['skip'] = 0
    data = urlencode({'action' : action, 'json' : json.dumps(json_parametros)}).encode()
    with closing(urlopen(url, data)) as response:
        respuesta = response.read().decode()
    # print(json.loads(respuesta))
    t_universo = json.loads(respuesta)['universe_size']
    stop = time.time()
    segundos = stop - start
    tam_pedazo = int(round(30 * 30 / segundos))
    num_pedazos = math.ceil(t_universo/tam_pedazo)
    print('Setting up..')
    print('starting process..')
    df_resp = None
    for i in range(0, num_pedazos):
        json_parametros['tamano_bin'] = tam_pedazo
        json_parametros['skip'] = tam_pedazo * i
        data = urlencode({'action' : action, 'json' : json.dumps(json_parametros)}).encode()
        with closing(urlopen(url, data)) as response:
            respuesta = response.read().decode()
        try:
            print(json.loads(respuesta)['long_msg'])
        except:
            print(json.loads(respuesta)['status'])
        df = pd.DataFrame.from_dict(json.loads(respuesta)['sample'])
        if df_resp is None:
            df_resp = df
        else:
            df_resp = df_resp.append(df).reset_index(drop=True)
        avance = round(((i + 1)/num_pedazos) * 100, 2)
        if avance >= 100:
            print(str(avance) + " % completed.")
            print("wrapping up..")
        else:
            print(str(avance) + " % completed.")
            print("downloading..")
    if 's' in json_parametros:
        if int(json_parametros['s']) < df_resp.shape[0]:
            drop_indices = np.random.choice(df_resp.index, df_resp.shape[0] - int(json_parametros['s']), replace=False)
            df_resp = df_resp.drop(drop_indices)
    respuesta = json.loads(json.dumps({'universe_size' : t_universo, 'sample' : json.loads(df_resp.to_json())}))
    return respuesta


def API_powerModel(json_parametros):
    action = 'API_powerModel'
    data = urlencode({'action' : action, 'json' : json.dumps(json_parametros)}).encode()
    with closing(urlopen(url, data)) as response:
        respuesta = json.loads(response.read().decode())
    return respuesta


def comprobarJSONaDF(df_json):
    valido = True
    msj = "Sucess"
    try:
        df_nuevo = pd.read_json(df_json, convert_dates=False, convert_axes=False)
    except Exception as e:
        df_nuevo = None
        valido = False
        msj = "Error transforming json: " + str(e)
    return df_nuevo, valido, msj