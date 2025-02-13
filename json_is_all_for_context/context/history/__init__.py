from .. import Context

class HistoryStep:
  def get_json (self):
    pass

class History (Context):
  def append_history_steps (self, steps: list[HistoryStep]):
    pass
