from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate
from transformers import AutoTokenizer

# prompt = ChatPromptTemplate.from_messages([
#   SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
#   HumanMessagePromptTemplate.from_template("{input}")
# ])

chatml = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "hi!"}
]

tokenizer = AutoTokenizer.from_pretrained("../DeepSeek-R1-Distill-Qwen-32B-bnb-4bit")
output = tokenizer.apply_chat_template(chatml, add_generation_prompt=True, tokenize=False)

print(output)
