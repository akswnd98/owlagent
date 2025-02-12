from chat_history import ChatHistory, ConcreteChatHistory, UserChatStep
from function_call_history import FunctionCallHistory, ConcreteFunctionCallHistory

class AgentAction:
  def get_json (self):
    pass

class AnswerAction (AgentAction):
  _answer: str

  def __init__ (self, answer):
    self._answer = answer

  def get_json (self):
    return {
      "answer": self._answer
    }

class FunctionCallAction (AgentAction):
  def get_json (self):
    return {
      "name": self._function_name,
      "arguments": self._arguments
    }

class ChatAgent:
  def invoke (self, chat_history: ChatHistory, function_call_history: FunctionCallHistory) -> AgentAction:
    pass

class ChatAgentExecutor:
  def invoke (self, human_input: str):
    pass

class ConcreteChatAgentExecutor (ChatAgentExecutor):
  _chat_history: ChatHistory
  _function_call_history: FunctionCallHistory
  _chat_agnet: ChatAgent

  def __init__ (self, chat_agent: ChatAgent):
    self._chat_history = ConcreteChatHistory()
    self._function_call_history = ConcreteFunctionCallHistory()
    self._chat_agnet = chat_agent

  def invoke (self, human_input: str):
    self._function_call_history = ConcreteFunctionCallHistory()
    self._chat_history.append_history(UserChatStep(human_input))
    agent_action = None
    while not isinstance(agent_action, AnswerAction):
      agent_action = self._chat_agnet.invoke(self._chat_history, self._function_call_history)
