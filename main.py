import os
import pyodbc
from dotenv import load_dotenv
from src.bcb_to_excel import busca_normas, DadosBusca

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

STR_CONN = f'DRIVER={os.getenv("DB_DRIVER")};SERVER={os.getenv("DB_SERVER")};DATABASE={os.getenv("DB_DATABASE")};UID={os.getenv("DB_USERNAME")};PWD={os.getenv("DB_PASSWORD")}'

MAX_NUM = 90000
SO_NOVAS = True
TIPOS = [
    "Ato de Diretor",
    "Ato do Presidente",
    "Ato Normativo Conjunto",
    "Carta Circular",
    "Circular",
    "Comunicado",
    "Comunicado Conjunto",
    "Decisão Conjunta",
    "Instrução Normativa BCB",
    "Instrução Normativa Conjunta",
    "Portaria Conjunta",
    "Resolução BCB",
    "Resolução",
    "Resolução CMN",
    "Resolução Conjunta",
    "Resolução Coremec"
]
TIPOS_ESPECIAIS = [
    "Ato de Diretor",
    "Ato Normativo Conjunto",
    "Ato do Presidente",
    "Comunicado",
    "Comunicado Conjunto",
    "Decisão Conjunta"
]

dados = DadosBusca(MAX_NUM, SO_NOVAS, TIPOS, TIPOS_ESPECIAIS)

conn = pyodbc.connect(STR_CONN)

busca_normas(conn, dados)

conn.close()