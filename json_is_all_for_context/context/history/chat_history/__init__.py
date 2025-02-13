from .. import History, HistoryStep

class ChatStep (HistoryStep):
  _role: str
  _content: str

  def __init__ (self, role: str, content: str):
    self._role = role
    self._content = content
  
  def get_json (self):
    return {"role": self._role, "content": self._content}

class UserChatStep (ChatStep):
  def __init__ (self, content: str):
    super().__init__("chat", content)

class AssistantChatStep (ChatStep):
  def __init__ (self, content: str):
    super().__init__("assistant", content)

class ChatHistory (History):
  _chat_steps: list[ChatStep]

  def __init__ (self):
    self._chat_steps = []

  def get_json (self):
    return list(map(lambda chat_step: chat_step.get_json(), self._chat_steps))
  
  def append_history_steps (self, chat_steps: list[ChatStep]):
    self._chat_steps += chat_steps
