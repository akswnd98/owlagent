from json_is_all_for_context.context.history import History
from json_is_all_for_context.context.history.chat_history import ChatHistory, ChatStep
from json_is_all_for_context.context.history.function_call_history import FunctionCallHistory, FunctionCallStep

class FunctionCallableHistory (History):
  _chat_history: ChatHistory
  _function_call_history: FunctionCallHistory

  def __init__ (self):
    self._chat_history = ChatHistory()
    self._function_call_history = FunctionCallHistory()

  def get_json (self):
    return {"chat_history": self._chat_history.get_json(), "function_call_history": self._function_call_history.get_json()}
  
  def append_history_steps (self, steps: list[ChatStep | FunctionCallStep]):
    for step in steps:
      self._append_history_step(step)

  def _append_history_step (self, step: ChatStep | FunctionCallStep):
    if isinstance(step, ChatStep):
      self._function_call_history = FunctionCallHistory()
      self._chat_history.append_history_steps([step])
    else:
      self._function_call_history.append_history_steps([step])
