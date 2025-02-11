
from langchain_community.chat_models.llamacpp import ChatLlamaCpp
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool

llm = ChatLlamaCpp(
  model_path="../DeepSeek-R1-Distill-Qwen-14B-Q4_0.gguf",
  n_ctx=65536
)

messages = [
  SystemMessage(content="You are a helpful assistant. You can call tool functions in JSON format if needed."),
  HumanMessage(content="please check current weather on seoul korea. i use celsius to describe degree.")
]

output = llm.invoke(
  messages,
  max_tokens=4096
)

print(output)
