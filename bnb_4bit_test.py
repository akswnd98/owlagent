from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
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

chat_llm = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate.from_template("""You will receive input that follows the [input schema].
You have to output following the [output schema].
Which means you have to call function.
You have access to the [functions].
I will provide all history at every step.
So call only one function call.
Additional function call? call at next step.
You can use information you know. apply for that information to give_final_answer function call.

[input schema]
{
  "type": "object",
  "properties": {
    "chat_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "user": {
            "type": "string",
            "description": "user input"
          },
          "assistant": {
            "type": "string",
            "description": "assistant answer which is return value of give_final_answer function call"
          }
        },
        "required": ["user", "assistant"],
        "additionalProperties": false
      }
    },
    "function_call_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "thought": {
            "type": "string"
          },
          "function_call": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "name of function to call"
              },
              "arguments": {
                "type": "object",
                "description": "arguments for function call"
              }
            },
            "required": ["name", "arguments"],
            "additionalProperties": false
          },
          "function_call_result": {
            "type": "object"
          }
        },
        "required": ["thought", "function_call", "function_call_result"],
        "additionalProperties": false
      }
    }
  },
  "required": ["chat_history", "function_call_history"],
  "additionalProperties": false
}

[output schema]
{
  "type": "object",
  "properties": {
    "thought": {
      "type": "string",
      "description": "The reason you called this function"
    },
    "function_call": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "name of function to call"
        },
        "arguments": {
          "type": "object",
          "description": "arguments for function call"
        }
      },
      "required": ["name", "arguments"],
      "additionalProperties": false
    }
  },
  "required": ["thought", "function_call"],
  "additionalProperties": false
}

[functions]
You have access to the following functions
---
function schema:
{
  "type": "object",
  "description": "function for send email",
  "properties": {
    "name": {
      "type": "string",
      "const": "send_email"
    },
    "arguments": {
      "type": "object",
      "properties": {
        "address": {
          "type": "string",
          "description": "target email address"
        },
        "subject": {
          "type": "string",
          "description": "title of this email"
        },
        "body": {
          "type": "string",
          "description": "main detail of this email"
        }
      },
      "required": ["address", "subject", "body"],
      "additionalProperties": false
    }
  },
  "required": ["name", "arguments"],
  "additionalProperties": false
}

return schema:
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "message indicating success or failure"
    }
  }
}
---
function schema:
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "const": "give_final_answer"
    },
    "arguments": {
      "type": "object",
      "properties": {
        "final_answer": {
          "type": "string",
          "description": "final answer. report for user input"
        }
      },
      "additionalProperties": false
    }
  },
  "required": ["name", "arguments"],
  "additionalProperties": false
}

return schema:
{
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
---
function schema:
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "const": "get_current_weather"
    },
    "arguments": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "format": {
          "type": "string",
          "description": "The temperature unit to use. Infer this from the users location. (choices: ["celsius", "fahrenheit"])"
        }
      },
      "required": ["location", "format"],
      "additionalProperties": false
    }
  },
  "required": ["name", "arguments"],
  "additionalProperties": false
}

return schema:
{
  "type": "object",
  "properties": {
    "temperature": {
      "type": "string"
    }
  },
  "required": ["temperature"],
  "additionalProperties": false
}
""", template_format="jinja2"),
  HumanMessagePromptTemplate.from_template("""{
  "chat_history": [
    "user": "{{input}}"
  ],
  "function_call_history": []
}

json=""", template_format="jinja2")
], template_format="jinja2")

chain = prompt | chat_llm

output = chain.invoke({"input": "who was the president of us in 2020?"})

print(output)
