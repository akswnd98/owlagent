from deepseek_r1_agent.prompt_template import generate_prompt_template
from deepseek_r1_agent.functions.give_final_answer import GiveFinalAnswer

prompt_template = generate_prompt_template()
prompt_template = prompt_template.partial(functions=[GiveFinalAnswer().get_schema()])
a = prompt_template.format_prompt(input='hello')
print(a.text)
