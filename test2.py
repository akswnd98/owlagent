from prompt_template import generate_prompt_template
from prompt_template.function_schema_loader import JsonFileFunctionSchemaLoader
import os

print(generate_prompt_template([
  JsonFileFunctionSchemaLoader("./function_schemas/give_final_answer.json"),
  JsonFileFunctionSchemaLoader("./function_schemas/get_current_weather.json"),
  JsonFileFunctionSchemaLoader("./function_schemas/send_email.json")
]))