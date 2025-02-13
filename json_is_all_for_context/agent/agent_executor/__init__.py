from ...context.history import History
from ...agent import Agent
from ...context.history.chat_history import UserChatStep, AssistantChatStep
from ...context.history.function_call_history import FunctionCallStep
from ...agent import AnswerAction, FunctionCallAction, Function
from typing import Callable

class HistoryGenerator:
  def generate (self) -> History:
    pass

class AgentExecutor:
  def invoke (self, input: str):
    pass

  def bind_functions (self, functions: list[Function]):
    pass

class SimpleAgentExecutor:
  _history: History
  _agent: Agent
  _function_key_lambda_map: dict[str, Callable]

  def __init__ (self, agent: Agent, history_generator: HistoryGenerator):
    self._agent = agent
    self._history = history_generator.generate()

  def invoke (self, input: str):
    self._history.append_history_steps([UserChatStep(input)])
    agent_action: AnswerAction | FunctionCallAction | None = None
    while True:
      agent_action = self._agent.invoke(self._history)
      if isinstance(agent_action, AnswerAction):
        break
      
      agent_action_json = agent_action.get_json()
      function_lambda = self._function_key_lambda_map[agent_action_json["function_call"]["name"]]
      function_return = function_lambda(agent_action_json["function_call"]["arguments"])
      self._history.append_history_steps([
        FunctionCallStep(
          agent_action_json["thought"],
          agent_action_json["function_call"]["name"],
          agent_action_json["function_name"]["arguments"],
          function_return
        )
      ])
    
    self._history.append_history_steps([AssistantChatStep(agent_action.get_json())])
  
  def bind_functions (self, functions: list[Function]):
    for function in functions:
      self._function_key_lambda_map[function.get_function_name()] = lambda arguments: function.call(arguments)

    self._agent.bind_functions(functions)
