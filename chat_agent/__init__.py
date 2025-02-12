class AgentAction:
  pass

class ChatAgent:
  def invoke (chat_history: ChatHistory, function_call_history: FunctionCallHistory) -> AgentAction:
    pass

class ChatAgentExecutor:
  def invoke (human_input: str):
    pass
