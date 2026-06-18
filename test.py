import requests
import dotenv
import os

dotenv.load_dotenv()

def buscar_bolsa_familia(mes_ano, codigo_ibge, pagina):
    
    headers = {
    os.getenv("KEY"): os.getenv("API_KEY")
    }

    params = {
    "mesAno": "202601",
    "codigoIbge": "3550308",
    "pagina": 1
    }

    url = "https://api.portaldatransparencia.gov.br/api-de-dados/novo-bolsa-familia-por-municipio"

    response = requests.get(url, headers=headers, params=params)


    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Erro ao acessar a API. Código: {response.status_code}")
        return None