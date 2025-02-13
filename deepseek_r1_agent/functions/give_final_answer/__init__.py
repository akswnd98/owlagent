from json_is_all_for_context.agent import Function, SimpleFunction
import json
import os

class GiveFinalAnswer (SimpleFunction):
  def __init__ (self):
    super().__init__("give_final_answer", json.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/schema.json")))

  def call (self, arguments):
    return arguments["final_answer"]
