from json_is_all_for_context.agent import Function, SimpleFunction
import json
import os

class GetCurrentWeather (SimpleFunction):
  def __init__ (self):
    super().__init__(json.dumps(open(f"{os.path.dirname(os.path.abspath(__file__))}/schema.json").read()))

  def call (self, arguments):
    return arguments["final_answer"]
