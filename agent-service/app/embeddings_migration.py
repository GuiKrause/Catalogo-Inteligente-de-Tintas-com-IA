import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")

client = OpenAI(api_key=OPENAI_API_KEY)
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

def gerar_texto_para_embedding(tinta):
    return f"""
    Tinta {tinta[1]}. {tinta[2]}. Cor: {tinta[3]}. 
    Tipo: {tinta[4]}. Superfície: {tinta[5]}. Ambiente: {tinta[6]}. 
    Acabamento: {tinta[8]}. Linha: {tinta[9]}. Odor: {tinta[10]}.
    Lavável: {'Sim' if tinta[15] else 'Não'}. Anti-mofo: {'Sim' if tinta[14] else 'Não'}.
    """.strip()

cur.execute("SELECT * FROM paints WHERE embedding IS NULL")
tintas = cur.fetchall()

print(f"Processando {len(tintas)} tintas...")

for tinta in tintas:
    tinta_id = tinta[0]
    texto_rico = gerar_texto_para_embedding(tinta)
    
    response = client.embeddings.create(
        model=EMBEDDINGS_MODEL,
        input=texto_rico
    )
    embedding = response.data[0].embedding
    
    cur.execute(
        "UPDATE paints SET embedding = %s WHERE id = %s",
        (embedding, tinta_id)
    )
    conn.commit()
    print(f"Atualizado: {tinta[1]}")

cur.close()
conn.close()
print("Migração concluída!")