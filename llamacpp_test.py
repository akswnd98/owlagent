
from langchain_community.chat_models.llamacpp import ChatLlamaCpp
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from deepseek_r1_agent.prompt_template import generate_prompt_template
from deepseek_r1_agent.functions.get_current_weather import GetCurrentWeather
from deepseek_r1_agent.functions.give_final_answer import GiveFinalAnswer
import json
from langchain_community.llms.llamacpp import LlamaCpp
from llama_cpp import Llama, ChatCompletionRequestUserMessage, ChatCompletionRequestAssistantMessage
from transformers import AutoTokenizer

llm = Llama(
  model_path="../DeepSeek-R1-Distill-Qwen-14B-GGUF/DeepSeek-R1-Distill-Qwen-14B-Q4_0.gguf",
  n_ctx=15000,
  n_gpu_layers=-1,
  temperature=0.6,
  max_tokens=1024,
  n_batch=512
)

tokenizer = AutoTokenizer.from_pretrained("../DeepSeek-R1-Distill-Qwen-14B-GGUF")

prompt_template = generate_prompt_template()
prompt_template = prompt_template.partial(functions=json.dumps(list(map(lambda function: function.get_schema(), [GiveFinalAnswer(), GetCurrentWeather()]))))
message = prompt_template.format_prompt(input=json.dumps({
  "chat_history": [
    {"role": "user", "content": "what is the temperature in seoul now?"}
  ],
  "function_call_history": []
}))


print(message.text)
# chat_input: str = tokenizer.apply_chat_template(
#   [{"role": "user", "content": message.text}],
#   # generate_prompt_template=True,
#   tokenize=False
# )
chat_input = message.text
chat_input = f"{chat_input}<think>\n"
print(chat_input)
output = llm(chat_input, max_tokens=4096, temperature=0.6)

print(output)
