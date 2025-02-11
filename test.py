import json

data = json.dumps({
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "Get current weather in given location with format",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "format": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["name", "age"]
    }
  }
})

print(data)
