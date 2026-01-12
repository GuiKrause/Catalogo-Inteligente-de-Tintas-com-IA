from langchain.agents import create_openai_functions_agent, AgentExecutor
from .clients import clients
from .tools import tools
from .prompts import prompts

class AgentManager:
    def __init__(self):
        self.llm = clients.llm
        self.tools = tools
        self.prompt = self._setup_prompt()
        self._executor = None

    def _setup_prompt(self):
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        return ChatPromptTemplate.from_messages([
            ("system", prompts.system_instructions),
            # O AgentExecutor espera 'chat_history' para memória
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}"),
            # Onde o agente armazena os passos das ferramentas
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    @property
    def executor(self) -> AgentExecutor:
        if self._executor is None:
            agent = create_openai_functions_agent(
                llm=self.llm, 
                tools=self.tools, 
                prompt=self.prompt
            )
            self._executor = AgentExecutor(
                agent=agent, 
                tools=self.tools, 
                verbose=True,
                handle_parsing_errors=True
            )
        return self._executor

    def run(self, question: str, chat_history: list = None) -> str:
        """
        Executa o agente de forma simples e retorna apenas a string final.
        """
        response = self.executor.invoke({
            "input": question,
            "chat_history": chat_history or []
        })
        
        return response["output"]

# Instância Singleton
agent_manager = AgentManager()