
from langchain_community.chat_models.llamacpp import ChatLlamaCpp
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

llm = ChatLlamaCpp(
  model_path="../DeepSeek-R1-Distill-Qwen-32B-Q4_0.gguf",
  n_ctx=65536,
  n_gpu_layers=-1
)

messages = [
  HumanMessage(content="please check current weather on seoul korea. i use celsius to describe degree.")
]

output = llm.invoke(
  messages,
  max_tokens=4096
)

print(output)
