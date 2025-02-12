class ChatStep:
  def get_json (self):
    pass

class ChatHistory:
  def get_json (self):
    pass

  def append_history (self, chat_step: ChatStep):
    pass

class UserChatStep (ChatStep):
  _content: str

  def __init__ (self, content: str):
    self._content = content

  def get_json (self):
    return {"role": "user", "content": self._content}

class AssistantChatStep (ChatStep):
  _content: str

  def __init__ (self, content: str):
    self._content = content

  def get_json (self):
    return {"role": "assistant", "content": self._content}

class ConcreteChatHistory (ChatHistory):
  _chat_list: list[ChatStep]

  def __init__ (self):
    self._chat_list = []

  def get_json (self):
    return list(map(lambda chat_step: chat_step.get_json(), self._chat_list))
  
  def append_history (self, chat_step: ChatStep):
    self._chat_list.append(chat_step)
