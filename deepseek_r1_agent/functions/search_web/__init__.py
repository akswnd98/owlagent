from json_is_all_for_context.agent import Function, SimpleFunction
import json
import os
from langchain_community.utilities import SearxSearchWrapper

class SearchWeb (SimpleFunction):
  _search: SearxSearchWrapper

  def __init__ (self):
    super().__init__("search_web", json.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/schema.json")))
    self._search = SearxSearchWrapper(searx_host="http://localhost:20202", unsecure=True)

  def call (self, arguments):
    return self._search.run(arguments["search_query"])
