from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver 
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from sqlalchemy import text
from openai import OpenAI

from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AGENT_MODEL = os.getenv("AGENT_MODEL")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = ChatOpenAI(model=AGENT_MODEL)

db = SQLDatabase.from_uri(DATABASE_URL)

system_msg = f"""
    Você é o "Consultor Inteligente de Tintas", um assistente que faz consultas sobre tintas interagindo com um banco de dados SQL.
    Seu objetivo é guiar o usuário desde a intenção subjetiva até o orçamento e visualização final.

    - Sempre que receber uma pergunta do usuário crie uma query {db.dialect} sintaticamente correta.
    - Sempre que precisar filtrar por colunas de texto (como cor, acabamento ou ambiente) e não tiver certeza do termo exato, prefira usar o operador ILIKE com o símbolo % para buscas parciais. Por exemplo, em vez de cor = 'Branco', use cor ILIKE '%Branc%' para capturar 'Branco', 'branca' ou 'esbranquiçado'.
    - Seja objetivo nas respostas e forneça informações detalhadas apenas sob demanda do usuário.
    - Ao buscar cores ou nomes, nunca use o operador '='.
    - Sempre use 'ILIKE' para ignorar maiúsculas/minúsculas.
    - Adicione '%' antes e depois do termo (ex: ILIKE '%branc%').
    - Se uma consulta SQL retornar zero resultados, você deve OBRIGATORIAMENTE usar a ferramenta 'semantic_search' para encontrar os nomes corretos antes de tentar o SQL novamente.
    - Se o usuário usar termos subjetivos ("calmo", "moderno", "cor de areia") ou variações gramaticais ("tintas esverdeadas"), use PRIORITARIAMENTE a ferramenta 'semantic_search'.
    - Se o usuário pedir dados exatos ("preço da tinta X", "estoque de branco neve", "média de preços"), use as ferramentas de SQL.
    - Após encontrar nomes de tintas via busca semântica, use o SQL para buscar detalhes técnicos (preço, rendimento, código) dessas tintas específicas.
    - Jamais rode um comando DML (INSERT, UPDATE, DELETE, DROP etc.) para manipular a tabela.

    SUAS FERRAMENTAS:
    - 'semantic_search': Utilize sempre que o usuário pedir tintas utilizando termos que não estão relacionados a descrição da tinta como: sentimentos, emoções e sensações.
    - 'dalle_tool': Utilize quando o usuário pedir para gerar uma imagem com a tinta escolhida".
    - 'sql_db_list_tables': A entrada é uma string vazia; a saída é uma lista das tabelas existentes no banco de dados, separadas por vírgulas.
    - 'sql_db_schema': A entrada para esta ferramenta é uma lista de tabelas separadas por vírgulas; a saída é o esquema (estrutura) e linhas de exemplo dessas tabelas. Certifique-se de que as tabelas realmente existem chamando a ferramenta sql_db_list_tables primeiro! Exemplo de entrada: tabela1, tabela2, tabela3.
    - 'sql_db_query': A entrada para esta ferramenta deve ser uma consulta SQL detalhada e correta; a saída será o resultado vindo do banco de dados. Se a consulta estiver incorreta, uma mensagem de erro será retornada. Caso um erro seja retornado, reescreva a consulta, verifique-a e tente novamente. Se encontrar um problema de "Coluna desconhecida 'xxxx' na lista de campos" (Unknown column 'xxxx' in 'field list'), use a ferramenta sql_db_schema para consultar os campos corretos da tabela.
    - 'sql_db_query_checker': Use esta ferramenta para verificar detalhadamente se sua consulta está correta antes de executá-la. Sempre utilize esta ferramenta antes de executar qualquer consulta"""

system_prompt = SystemMessage(content=system_msg)

@tool
def semantic_search(query_usuario: str) -> list:
    """
    Recupera dados técnicos e descritivos das tintas mais próximas ao termo buscado.
    Use o retorno para formular uma recomendação personalizada.
    """
    
    resp = client.embeddings.create(
        model=os.getenv("EMBEDDINGS_MODEL"),
        input=query_usuario
    )
    embedding_query = resp.data[0].embedding

    with db._engine.connect() as conn:
        sql = text("""
            SELECT *
            FROM tintas 
            ORDER BY embedding <=> :val
        """)
        
        result = conn.execute(sql, {"val": str(embedding_query)})
        return [dict(r._mapping) for r in result.fetchall()]


api_wrapper = DallEAPIWrapper()
dalle_tool = OpenAIDALLEImageGenerationTool(api_wrapper=api_wrapper)

toolkit = SQLDatabaseToolkit(db=db, llm=model)
sql_tools = toolkit.get_tools()

tools = sql_tools + [dalle_tool, semantic_search]

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    checkpointer=InMemorySaver(),
)

def run_sql_agent(question: str) -> str:

    final_answer = ""

    for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        {"configurable": {"thread_id": "1"}},  
        stream_mode="values",
    ):
        last_message = step["messages"][-1]

        if isinstance(last_message, AIMessage):
            final_answer = last_message.content

    return final_answer


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class RecommendationResponse(BaseModel):
    answer: str

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: QuestionRequest):
    answer = run_sql_agent(request.question)
    return RecommendationResponse(answer=answer)