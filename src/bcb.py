#python -m pip install openpyxl
import requests
import json
import urllib3
import pandas as pd
import pyodbc

urllib3.disable_warnings()

TIPOS_ESPECIAIS = [
    "Ato de Diretor",
    "Ato Normativo Conjunto",
    "Ato do Presidente",
    "Comunicado",
    "Comunicado Conjunto",
    "Decisão Conjunta"
]

class DadosBusca:
    def __init__(self, max_num, so_novas, tipos):
        self.max_num = max_num
        self.so_novas = so_novas
        self.tipos = tipos

############################################################################
# get_url: Função para fazer a requisição GET e retornar os dados JSON
def get_url(url):
  try:
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

    return response.json()  # Carrega os dados JSON
  except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    return None

############################################################################
# busca_normas: Função para buscar as normas no site do Banco Central
def busca_normas(conn, dados_busca):
    try:
        print("Iniciando busca")
        for tipo in dados_busca.tipos:
            print(f"Buscando em: {tipo}")
            tipo_url = tipo.replace(" ", "%20")
            numeros = range(1, dados_busca.max_num + 1)
            if dados_busca.so_novas:
                ult_numero = BuscaUltimoNumero(tipo, conn)
                if ult_numero:
                    numeros = range(ult_numero + 1, dados_busca.max_num + 1)
              
            normaEncontrada = -1  
            for numero in numeros:

                registro = busca_norma(tipo, numero, conn)
                if registro:
                    normaEncontrada = 0
                elif normaEncontrada >= 0 or numeros[0] > 1:
                    normaEncontrada += 1

                if normaEncontrada >= (5 if tipo != "Comunicado" else 12):
                    break

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar a norma {numero} do tipo {tipo}: {e}")

############################################################################
# BuscaNorma: Função para buscar uma norma específica
def busca_norma(tipo, numero, conn):
    url = f"https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1={tipo}&p2={numero}"
    if tipo in TIPOS_ESPECIAIS:
        url = f"https://www.bcb.gov.br/api/conteudo/app/normativos/exibeoutrasnormas?p1={tipo}&p2={numero}"
    tipo_url = tipo.replace(" ", "%20")
    link = f"https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo={tipo_url}&numero={numero}"

    retorno = get_url(url)    
            
    if retorno and retorno.get("conteudo", []):          
        print(link)
        for conteudo in retorno.get("conteudo", []):
            registro = (conteudo.get("Titulo"),
                            conteudo.get("Tipo"),
                            conteudo.get("Documentos"),
                            conteudo.get("DOU"),
                            conteudo.get("Id"),
                            conteudo.get("Data"),
                            conteudo.get("DataTexto"),
                            conteudo.get("Numero"),
                            conteudo.get("VersaoNormativo"),
                            conteudo.get("Assunto"),
                            conteudo.get("Texto"),
                            conteudo.get("NormasVinculadas"),
                            conteudo.get("Referencias"),
                            conteudo.get("Atualizacoes"),
                            conteudo.get("Revogado"),
                            conteudo.get("Cancelado"),
                            conteudo.get("Voto"),
                            link,
                            json.dumps(conteudo))
            ToSQLServer(registro, conn)    
        return registro 
    else:   
        return None

############################################################################
# ToSQLServer: Função para inserir os dados no SQL Server
def ToSQLServer(dados, conn):   
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Normas WHERE Id = ?", dados[4])
#    cursor.executemany("""
    cursor.execute("""
        INSERT INTO Normas (Titulo, Tipo, Documentos, DOU, Id, Data, DataTexto, Numero, VersaoNormativo, Assunto, Texto, NormasVinculadas, Referencias, Atualizacoes, Revogado, Cancelado, Voto, Link, Conteudo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dados)
    conn.commit()
    cursor.close()

############################################################################
# BuscaUltimoNumero: Função para buscar o último número de uma norma
def BuscaUltimoNumero(tipo, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Numero) FROM Normas WHERE Tipo = ?", tipo)
    ultimo_numero = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return ultimo_numero

############################################################################
# Início do programa
# busca_normas()

"""
"Titulo": "Resolução BCB N° 285",
"Tipo": "Resolução BCB",
"Documentos": null,
"DOU": "Publicada no DOU de 20/1/2023, Seção 1, p. 40-43. ",
"Id": 51967,
"Data": "2023-01-19T12:31:00Z",
"DataTexto": "19/1/2023 09:31",
"Numero": 285,
"VersaoNormativo": 2,
"Assunto": "Dispõe sobre a constituição e o funcionamento de grupos de consórcio.",
"NormasVinculadas": "RESOLUÇÃO BCB;@362;@2023;#CARTA CIRCULAR;@3776;@2016;#CARTA CIRCULAR;@3671;@2014;#CIRCULAR;@4009;@2020;#CIRCULAR;@3936;@2019;#CIRCULAR;@3785;@2016;#CIRCULAR;@3618;@2012;#CIRCULAR;@3558;@2011;#CIRCULAR;@3524;@2011;#CIRCULAR;@3432;@2009;#CIRCULAR;@3394;@2008;#CIRCULAR;@3023;@2001;#CIRCULAR;@2381;@1993;#RESOLUÇÃO BCB;@381;@2024;#INSTRUÇÃO NORMATIVA BCB;@525;@2024;#",
"Referencias": "Lei nº 11.795/2008.;#Revoga, a partir de 1º/7/2024, Circulares BCB ns. 2.381/1993, 3.023/2001, 3.394/2008, 3.432/2009, 3.524/2011, 3.558/2011, 3.618/2012, 3.785/2016, 3.936/2019 e 4.009/2020.;#Revoga, a partir de 1º/7/2024, Cartas Circulares BCB ns. 3.671/2014 e 3.776/2016.;#",
"Atualizacoes": "Resolução BCB nº 362/2023 - Nova redação: art. 22, incisos I e IV; art. 30, caput; art. 32, incisos II e III e parágrafo único; art. 33, caput e parágrafo único; art. 49, caput, incisos VI, “e”, VII, VIII; e arts. 57 e 59. Inclusão: art. 12, parágrafo único; art. 22, inciso I, “a”, “b” e “c”; arts. 25-A e 25-B; art. 30, incisos I e II e parágrafo único; art. 32-A; art. 33, incisos I e II; e art. 49, inciso IX e §§ 1º e 2º. Revogação: art. 21, parágrafo único; art. 25; art. 33, parágrafo único, incisos I e II; e art. 49, parágrafo único.;#",
"Revogado": false,
"Cancelado": false,
"Texto": 
"Voto":
"""