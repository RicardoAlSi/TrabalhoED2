import dotenv
from requests import get 
from os import getenv

dotenv.load_dotenv()

header_GOV = {getenv("KEY"):getenv("API_KEY")}

def reqIbge():
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
    
    response = get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Algo de errado com a API: {response.status_code}")
        return

    return data
    

def getIbgeCodigo(nome):
    
    data = reqIbge()
    
    municipios = list()
    municipios_nomes = list()
    
    count = 0
    
    for municipio in data:
        if nome.lower() in municipio['nome'].lower():
            print(f"{count} Nome: {municipio['nome']}; Código IBGE: {municipio["id"]}")
            municipios.append(municipio['id']) 
            municipios_nomes.append(municipio['nome'])
            if count >=20:
                break
            count +=1
    if len(municipios) > 1:
        escolha = int(input("Digite o número correspondente ao seu municipio: "))
        codigoIbge = municipios[escolha]
        nome_muni = municipios_nomes[escolha]
    elif len(municipios) ==1:
        codigoIbge = municipios[0]
        nome_muni = municipios_nomes[0]
    else: 
        print("Municipio não encontrado!")
    return codigoIbge, nome_muni

def getInfoEstado(estado):
    data = reqIbge()
    
    populacao = 0
    ids = list()
    for municipio in data:
        
        uf = municipio.get('regiao-imediata', {}).get('regiao-intermediaria', {}).get('UF', {}).get('sigla').upper()
        
        if estado.upper() in uf:
            ids.append(municipio['id'])
            populacao += int(getInfoMunicipio(municipio['id']))
    
    return populacao, ids
    

def getInfoMunicipio(codigoIbge):
    url = f"https://apisidra.ibge.gov.br/values/t/9922/n6/{codigoIbge}/v/allxp/p/2022?formato=json"  
    
    response = get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Algo de errado com a API: {response.text} {response.status_code} ")
        return
    
    populacao = data[2]['V']
    domicilio = data[1]['V']
    
    return populacao, domicilio
    
            
def getBolsaFamiliaMunicipio(mesAno, codigoIbge, page=1):
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

def getBolsaFamiliaEstado(estado, mesAno):
    populacao, ids=getInfoEstado(estado=estado)
    
    beneficiarios = 0
    
    for id in ids:
        _, beneficiariosMuni = int(getBolsaFamiliaMunicipio(mesAno=mesAno, codigoIbge=id))
        beneficiarios += beneficiariosMuni
    
    return populacao, beneficiarios 

def main():
    
    option = int(input("Digite números das respectivas funções \n1 - Razão pessoas que necessitam do auxilio / população do municipio\n2 - Razão pessoas que necessitam do aúxilio / população do estado\n"))
    
    match (option):
        case 1:
            sla = input("Qual municipio você quer saber a razão de familias para familias beneficiadas no bolsa familia?\n")
            sla1= input("De qual mês e ano? Preencha AAAAMM. Ex.: 202601\n")
            
            codigoIbge, nome = getIbgeCodigo(sla)
            
            _, familias = getInfoMunicipio(codigoIbge=codigoIbge)
            
            qtdBene = int(getBolsaFamiliaMunicipio(mesAno=sla1, codigoIbge=codigoIbge))
            
            print(f"{nome} tem a razão de {(qtdBene/int(familias))*100:.2f}%")
        case 2:
            state = input("Qual estado quer ver? Digite a sigla (Ex.: SP)\n")
            
            ano = input("De qual mês e ano? Preencha AAAAMM. Ex 202601\n")
            
            populacao, beneEstado = getBolsaFamiliaEstado(mesAno=ano, estado=state)
            print(f"{beneEstado} familias vivem do auxilio, com isso {(beneEstado/populacao)*100:.2f}% da população vive com aúxilio do Bolsa Familia")
            
main()