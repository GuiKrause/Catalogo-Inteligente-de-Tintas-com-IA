from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from .config import settings

from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from .config import settings

class Clients:
    def __init__(self):
        # SDK Original
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Chat Model
        self.llm = ChatOpenAI(
            model=settings.AGENT_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )

        # Banco de Dados
        self.db = SQLDatabase.from_uri(settings.DATABASE_URL)

clients = Clients()