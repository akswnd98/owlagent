from langchain_core.prompts import PromptTemplate
import os
import json

def generate_prompt_template ():
  current_dir = os.path.dirname(os.path.abspath(__file__))

  with open(f"{current_dir}/prompt_template.txt", "r") as f:
    template = PromptTemplate.from_template(template=f.read(), template_format="jinja2")
  
  with open(f"{current_dir}/input_schema.json", "r") as f:
    input_schema_json = json.load(f)

  with open(f"{current_dir}/output_schema.json", "r") as f:
    output_schema_json = json.load(f)

  return template.partial(
    input_schema=json.dumps(input_schema_json),
    output_schema=json.dumps(output_schema_json)
  )
