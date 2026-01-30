import geopandas as gpd
import requests
from io import BytesIO
import os
from config import data_folder
from utils.save_shp import save_shp_custom
from utils.load_shp import load_shp

#! transformar em CLASS

def sc_file_path(file_name):
    sc_path = os.path.join(
        data_folder,
        'setores_censitarios',
        file_name
    )
    return sc_path

def download_setores_censitarios():
    file = sc_file_path('setores_censitarios.shp')
    
    if os.path.exists(file):
        print('Retornando arquivo salvo')
        return gpd.read_file(file)

    print('Carregando do IBGE')

    url = ('https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_preliminares/malha_com_atributos/setores/shp/UF/SP/SP_Malha_Preliminar_2022.zip')

    with requests.get(url, stream = True) as r:
        content = BytesIO(r.content)
        gdf_setores_censitarios = gpd.read_file(content)

    save_shp_custom(gdf_setores_censitarios, file)

    return gdf_setores_censitarios

def setores_censitarios_final():
    file = sc_file_path('setores_censitarios_treated.shp')

    if os.path.exists(file):
        print('Retornando arquivo salvo')
        return gpd.read_file(file)

    setores_censitarios = download_setores_censitarios()
    print('Inicializando tratamento')
    
    # Coluna de população do setor censitário.
    setores_censitarios = setores_censitarios.rename(columns={'v0001': 'pop_setor'})
    setores_censitarios['pop_setor'] = setores_censitarios['pop_setor'].astype(int)
    setores_censitarios= setores_censitarios.loc[setores_censitarios['pop_setor'] > 0]
    
    # Filtro para o município de São Paulo.
    setores_censitarios_sp = setores_censitarios[setores_censitarios['CD_MUN'] == '3550308'].copy()
    
    setores_censitarios_sp = setores_censitarios_sp.to_crs("EPSG:31983")

    #Dropar cols desnecessárias
    drop_cols={
        'CD_REGIAO',
        'NM_REGIAO', 
        'CD_UF', 
        'NM_UF',
        'CD_MICRO', 
        'NM_MICRO', 
        'CD_MESO', 
        'NM_MESO', 
        'CD_RGI', 
        'NM_RGI',
        'CD_RGINT', 
        'NM_RGINT', 
        'CD_CONCURB', 
        'NM_CONCURB',
        'v0002',
        'v0003', 
        'v0004', 
        'v0005', 
        'v0006', 
        'v0007',
        'NM_SUBDIST'
    }
    setores_censitarios_sp.drop(columns=drop_cols, inplace=True)
    
    #save
    save_shp_custom(setores_censitarios_sp, file)
    return setores_censitarios_sp
    

    
