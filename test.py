from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, BaseOutputParser
from langchain.output_parsers.structured import StructuredOutputParser
from langchain.output_parsers import OutputFixingParser
from pydantic import BaseModel, Field
from typing import Dict, Any

class FunctionCall (BaseModel):
  name: str
  arguments: Dict[str, Any]

class Model (BaseModel):
  thought: str
  function_call: FunctionCall

class JsonExtractor (BaseOutputParser):
  def parse (self, text: str):
    start_index = text.find("```json")
    end_index = text.rfind("```")
    return text[start_index + 8: end_index]

parser = StrOutputParser() | JsonExtractor() | JsonOutputParser(pydantic_object=Model)

a = parser.invoke("""lksjdlfjawlkjfsasdf
                    ```json
{
  "thought": "I need to get the current weather in Seoul before sending an email about it.",
  "function_call": {
    "name": "get_current_weather",
    "arguments": {
      "location": "Seoul",
      "format": "celsius"
    }
  }
}```gasdfljk
                    asldfjwoji""")

print(a["thought"], a["function_call"], a["function_call"]["arguments"])
