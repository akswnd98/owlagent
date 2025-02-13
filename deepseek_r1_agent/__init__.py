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
from deepseek_r1_agent.functions.give_final_answer import GiveFinalAnswer

class FunctionCall (BaseModel):
  name: str
  arguments: Dict[str, Any]

class Model (BaseModel):
  thought: str
  function_call: FunctionCall

class ThinkCutter (BaseOutputParser):
  def parse (self, text: str):
    start_index = text.find("</think>") + 1
    return text[start_index: ]

class JsonExtractor (BaseOutputParser):
  def parse (self, text: str):
    start_index = text.find("```json") + 8
    end_index = text.rfind("```")
    return text[start_index: end_index]

class DeepseekR1Agent (Agent):
  _gguf_path: str
  _functions: list[Function]
  _prompt_template: PromptTemplate
  _llm: ChatLlamaCpp

  def __init__ (self, gguf_path: str):
    super().__init__()
    self._gguf_path = gguf_path
    self._functions = []
    self.bind_functions([GiveFinalAnswer()])
    self._llm = ChatLlamaCpp(
      model_path=self._gguf_path,
      n_ctx=65536,
      n_gpu_layers=-1
    ) | StrOutputParser() | ThinkCutter() | JsonExtractor() | JsonOutputParser(pydantic_object=Model)

  def invoke (self, history: FunctionCallableHistory) -> AgentAction:
    input = json.dumps(history.get_json())
    messages = [HumanMessage(content=self._prompt_template.format_prompt(input=input).text)]
    print(f"input: {messages[0].content}")
    output_json = self._llm.invoke(messages, max_tokens=4096)
    if output_json["function_call"]["name"] == "give_final_answer":
      return AnswerAction(output_json["function_call"]["arguments"]["final_answer"])
    else:
      return FunctionCallAction(output_json)

  def bind_functions (self, functions: list[Function]):
    self._functions += functions
    self._prompt_template = generate_prompt_template()
    self._prompt_template = self._prompt_template.partial(
      functions=list(map(lambda function: json.dumps(function.get_schema()), self._functions))
    )

    
