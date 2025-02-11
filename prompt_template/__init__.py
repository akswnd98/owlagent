from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, StringPromptTemplate, PromptTemplate, BasePromptTemplate
import os
import json
from .function_schema_loader import FunctionSchemaLoader

def generate_prompt_template (function_schema_loaders: list[FunctionSchemaLoader]):
  current_dir = os.path.dirname(os.path.abspath(__file__))

  with open(f"{current_dir}/prompt_template.txt", "r") as f:
    template = PromptTemplate.from_template(template=f.read(), template_format="jinja2")
  
  with open(f"{current_dir}/input_schema.json", "r") as f:
    input_schema_json = json.load(f)

  with open(f"{current_dir}/output_schema.json", "r") as f:
    output_schema_json = json.load(f)
  
  function_schemas = list(map(lambda loader: loader.load(), function_schema_loaders))

  return template.partial(
    input_schema=json.dumps(input_schema_json),
    output_schema=json.dumps(output_schema_json),
    functions=json.dumps(function_schemas)
  )
