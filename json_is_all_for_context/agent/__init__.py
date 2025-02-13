from ..context.history import History

class AgentAction:
  def get_json (self):
    pass

class AnswerAction (AgentAction):
  _answer: str

  def __init__ (self, answer):
    self._answer = answer

  def get_json (self):
    return self._answer

class FunctionCallAction (AgentAction):
  _json: any

  def __init__ (self, json):
    self._json = json

  def get_json (self):
    return self._json

class Function:
  def call (self, arguments):
    pass

  def get_function_name (self) -> str:
    pass

  def get_schema (self) -> dict:
    pass

class SimpleFunction (Function):
  _function_name: str
  _function_schema: any

  def __init__ (self, function_name: str, function_schema: dict):
    self._function_name = function_name
    self._function_schema = function_schema

  def get_function_name (self):
    return self._function_name

  def get_schema (self) -> dict:
    return self._function_schema

class Agent:
  def invoke (self, history: History) -> AgentAction:
    pass

  def bind_functions (self, functions: list[Function]):
    pass
