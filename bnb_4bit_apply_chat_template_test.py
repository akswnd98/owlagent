from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate

model_path = "../DeepSeek-R1-Distill-Qwen-32B-bnb-4bit"

bnb_config = BitsAndBytesConfig(
  load_in_4bit=True,
  # bnb_4bit_use_double_quant=True,
  # bnb_4bit_quant_type="nf4",
  # bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
  model_path,
  device_map="auto",
  quantization_config=bnb_config
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

pipe = pipeline(
  "text-generation",
  model=model,
  tokenizer=tokenizer,
  max_new_tokens=2048,
  return_full_text=False
)

llm = HuggingFacePipeline(pipeline=pipe)

chatml = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "hi!"}
]

tokenizer = AutoTokenizer.from_pretrained("../DeepSeek-R1-Distill-Qwen-32B-bnb-4bit")
inputs = tokenizer.apply_chat_template(chatml, add_generation_prompt=True, tokenize=False)


output = llm.invoke(inputs)

print(output)
