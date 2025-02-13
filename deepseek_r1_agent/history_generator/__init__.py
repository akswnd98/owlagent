from json_is_all_for_context.agent.agent_executor.history_generator import HistoryGenerator
from ..function_callable_history import FunctionCallableHistory

class DeepseekR1HistoryGenerator (HistoryGenerator):
  def generate (self):
    return FunctionCallableHistory()
