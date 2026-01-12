from langchain.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from sqlalchemy import text

from .clients import clients
from .config import settings

class ToolManager:
    def __init__(self):
        # 1. Instanciamos o DALL-E
        self.dalle_wrapper = DallEAPIWrapper(api_key=settings.OPENAI_API_KEY)
        self.dalle_tool = OpenAIDALLEImageGenerationTool(api_wrapper=self.dalle_wrapper)
        
        # 2. Instanciamos o Toolkit SQL
        self.sql_toolkit = SQLDatabaseToolkit(db=clients.db, llm=clients.llm)
        
    def get_semantic_search_tool(self):
        """
        Criamos a ferramenta de busca semântica dentro de um método 
        para que ela tenha acesso ao contexto da classe se necessário.
        """
        @tool
        def semantic_search(query: str) -> list:
            """
            Recupera dados técnicos e descritivos das tintas mais próximas ao termo buscado.
            Use sempre para termos subjetivos (ex: 'cor que traz paz', 'moderno').
            """
            # Busca o embedding via OpenAI
            resp = clients.openai.embeddings.create(
                model=settings.EMBEDDINGS_MODEL,
                input=query
            )
            embedding_query = resp.data[0].embedding

            # Consulta ao banco usando o cliente centralizado
            with clients.db._engine.connect() as conn:
                sql = text("""
                    SELECT *
                    FROM tintas 
                    ORDER BY embedding <=> :val
                """)
                result = conn.execute(sql, {"val": str(embedding_query)})
                return [dict(r._mapping) for r in result.fetchall()]
        
        return semantic_search

    def get_all_tools(self):
        """
        Retorna a lista completa de ferramentas para o AgentExecutor.
        """
        return self.sql_toolkit.get_tools() + [
            self.dalle_tool, 
            self.get_semantic_search_tool()
        ]

# Instância única para ser usada no agent.py
toolbox = ToolManager()
tools = toolbox.get_all_tools()