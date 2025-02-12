class FunctionCallStep:
  def get_json (self):
    pass

class FunctionCallHistory:
  def get_json (self):
    pass

class ConcreteFunctionCallStep (FunctionCallStep):
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

class ConcreteFunctionCallHistory (FunctionCallHistory):
  _function_call_list: list[FunctionCallStep]

  def __init__ (self):
    self._function_call_list = []

  def get_json (self):
    return list(map(lambda function_call_step: function_call_step.get_json(), self._function_call_list))
  
  def append_history (self, function_call_step: FunctionCallStep):
    self._chat_list.append(function_call_step)
