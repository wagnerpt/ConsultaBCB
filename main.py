import os
import pyodbc
from dotenv import load_dotenv
from src.bcb import busca_normas, busca_norma, DadosBusca

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

dados = DadosBusca(MAX_NUM, SO_NOVAS, TIPOS)

conn = pyodbc.connect(STR_CONN)

busca_normas(conn, dados)

#busca_norma("", 1, conn)

conn.close()