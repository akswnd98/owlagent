from .. import History, HistoryStep

class FunctionCallStep (HistoryStep):
  _thought: str
  _function_name: str
  _arguments: any
  _function_call_result: str

  def __init__ (self, thought: str, function_name: str, arguments: any, function_call_result: str):
    self._thought = thought
    self._function_name = function_name
    self._arguments = arguments
    self._function_call_result = function_call_result

  def get_json (self):
    return {
      "thought": self._thought,
      "function_call": {
        "name": self._function_name,
        "arguments": self._arguments
      },
      "function_call_result": self._function_call_result
    }

class FunctionCallHistory (History):
  _function_call_steps: list[FunctionCallStep]

  def __init__ (self):
    self._function_call_steps = []

  def get_json (self):
    return list(map(lambda function_call_step: function_call_step.get_json(), self._function_call_steps))
  
  def append_history_steps (self, function_call_steps: list[FunctionCallStep]):
    self._function_call_steps += function_call_steps
