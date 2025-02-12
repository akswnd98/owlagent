from ..chat_history import ChatHistory, ConcreteChatHistory
from ..function_call_history import FunctionCallHistory, ConcreteFunctionCallHistory
from ...chat_agent import ChatAgent

class ChatAgentExecutor:
  def invoke (self, input: str):
    pass

class ConcreteChatAgentExecutor (ChatAgentExecutor):
  _chat_history: ChatHistory
  _function_call_history: FunctionCallHistory
  _chat_agent: ChatAgent

  def __init__ (self):
    self._chat_history = ConcreteChatHistory()
    self._function_call_history = ConcreteFunctionCallHistory()

  def invoke (self, input: str):
    
