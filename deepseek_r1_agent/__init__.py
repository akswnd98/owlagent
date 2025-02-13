from json_is_all_for_context.context.history import History
from .function_callable_history import FunctionCallableHistory
from json_is_all_for_context.agent import Agent, AgentAction, FunctionCallAction, AnswerAction
from json_is_all_for_context.agent import Function
from .prompt_template import generate_prompt_template
from langchain_core.prompts import PromptTemplate
import json
from langchain_community.chat_models.llamacpp import ChatLlamaCpp
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, BaseOutputParser
from pydantic import BaseModel
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

class DeepseekR1Agent (Agent):
  _gguf_path: str
  _functions: list[Function]
  _prompt_template: PromptTemplate
  _llm: ChatLlamaCpp

  def __init__ (self, gguf_path: str):
    super().__init__()
    self._gguf_path = gguf_path
    self._prompt_template = generate_prompt_template()
    self._prompt_template.parital(functions=[])
    self._llm = ChatLlamaCpp(
      model_path=self._gguf_path,
      n_ctx=65536
    ) | StrOutputParser() | JsonExtractor() | JsonOutputParser(pydantic_object=Model)

  def invoke (self, history: FunctionCallableHistory) -> AgentAction:
    input=json.dumps(history.get_json())
    messages = [HumanMessage(content=input)]
    output_json = self._llm.invoke(messages, max_tokens=4096)
    if output_json["function_call"]["name"] == "give_final_answer":
      return AnswerAction(output_json["function_call"]["arguments"]["final_answer"])
    else:
      return FunctionCallAction(output_json)

  def bind_functions (self, functions: list[Function]):
    self._functions += functions
    self._prompt_template = generate_prompt_template()
    self._prompt_template.partial(
      functions=list(map(lambda function: json.dumps(function.get_schema), self._functions))
    )

    
