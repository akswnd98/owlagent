from json_is_all_for_context.agent import Function, SimpleFunction
import json
import os

class GetCurrentWeather (SimpleFunction):
  def __init__ (self):
    super().__init__("get_current_weather", json.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/schema.json")))

  def call (self, arguments):
    return "current temperature is 37 degree."
