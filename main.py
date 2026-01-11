from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langchain.messages import AIMessage
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AGENT_MODEL = os.getenv("AGENT_MODEL")

model = init_chat_model(AGENT_MODEL)

db = SQLDatabase.from_uri(DATABASE_URL)

toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()

system_prompt = """
Você é um SQL Agent especialista em tintas.
Seu objetivo é recomendar tintas adequadas consultando um banco de dados {dialect}.

Utilize exclusivamente consultas SELECT na tabela tintas. Interprete linguagem natural e sinônimos quando necessário.

Não invente informações nem retorne dados que não existam no banco.
Se não houver resultados, informe isso claramente e sugira ajustes nos critérios.

Retorne as recomendações de forma clara, explicando brevemente apenas o que foi solicitado, não retorne todos os dados de uma vez.
""".format(
    dialect=db.dialect,
)

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)

def run_sql_agent(question: str) -> str:

    final_answer = ""

    for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        last_message = step["messages"][-1]

        if isinstance(last_message, AIMessage):
            final_answer = last_message.content

    return final_answer


# API

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str

class RecommendationResponse(BaseModel):
    recommendation: str

@app.post("/recommend")
def re(request: QuestionRequest):
    answer = run_sql_agent(request.question)
    print(answer)
    return {"answer": answer}