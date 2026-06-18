import requests

def buscar_municipio_ibge(nome_cidade):
    
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/grajau"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
