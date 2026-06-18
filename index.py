import dotenv
from requests import get 
from os import getenv

dotenv.load_dotenv()

header_GOV = {getenv("KEY"):getenv("API_KEY")}

def getIbgeCodigo(nome):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
    
    response = get(url)
    
    municipios = list()
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Algo de errado com a API: {response.status_code}")
        return
    count = 0
    
    for municipio in data:
        if nome.lower() in municipio['nome'].lower():
            print(f"{count} Nome: {municipio['nome']}; Código IBGE: {municipio["id"]}")
            municipios.append(municipio['id']) 
            if count >=20:
                break
            count +=1
    if len(municipios) > 1:
        escolha = int(input("Digite o número correspondente ao seu municipio: "))
        codigoIbge = municipios[escolha]
    else: 
        codigoIbge = municipio[0]
    return codigoIbge

def getPopulacaoMunicipio(codigoIbge):
    url = f"https://apisidra.ibge.gov.br/values/t/9514/n6/{codigoIbge}/v/93/p/2022?formato=json"  
    
    response = get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Algo de errado com a API: {response.text} {response.status_code} ")
        return
    
    populacao = data[1]['V']
    
    return populacao

            
def getQtdBolsaFamiliaMunicipio(mesAno, codigoIbge, page=1):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/novo-bolsa-familia-por-municipio"
    
    params = {
        "mesAno": str(mesAno),
        "codigoIbge": str(codigoIbge),
        "pagina": int(page)
    }
    
    response = get(url, params=params, headers=header_GOV)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Algo de errado com a API: {response.text} {response.status_code}")
        return
        
    return data[0]['quantidadeBeneficiados']

def main():
    sla = input("Qual municipio você quer saber a razão de população para beneficiarios do bolsa familia?\n")
    sla1= input("De qual mês e ano? Preencha AAAAMM. Ex.: 202601\n")
    
    
    codigoIbge = getIbgeCodigo(sla)
    
    population = int(getPopulacaoMunicipio(codigoIbge=codigoIbge))
    
    qtdBene = int(getQtdBolsaFamiliaMunicipio(mesAno=sla1, codigoIbge=codigoIbge))
    
    print(f"Grajaú tem a razão de {qtdBene/population:.2f}%")

main()