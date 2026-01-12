from langchain.agents import create_agent
from langchain.messages import HumanMessage
from .clients import clients
from .tools import tools
from .prompts import prompts

class AgentManager:
    def __init__(self):
        self.llm = clients.llm
        self.tools = tools
        self._agent = None

    @property
    def agent(self):
        """
        Instancia o agente usando o novo padrão funcional.
        O state_modifier substitui a necessidade de um objeto Prompt separado.
        """
        if self._agent is None:
            # create_react_agent cria um grafo de execução pronto para uso
            self._agent = create_agent(
                model=self.llm,
                tools=self.tools,
                system_prompt=prompts.system_instructions
            )
        return self._agent

    def run(self, question: str, chat_history: list = None) -> str:
        """
        Executa o agente e retorna o conteúdo da última mensagem de IA.
        """
        # Preparando as mensagens no novo formato de lista de mensagens
        # Se você tiver histórico, pode concatenar aqui: (chat_history or []) + [...]
        messages = (chat_history or []) + [HumanMessage(content=question)]
        
        # O invoke agora recebe uma lista de mensagens dentro do dicionário de estado
        result = self.agent.invoke({"messages": messages})
        
        # O resultado contém todas as mensagens da execução; pegamos a última (IA)
        final_message = result["messages"][-1]
        
        return final_message.content

# Instância Singleton
agent_manager = AgentManager()