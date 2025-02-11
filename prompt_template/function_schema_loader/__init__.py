import json

class FunctionSchemaLoader:
  def load (self) -> dict:
    pass

class JsonFileFunctionSchemaLoader (FunctionSchemaLoader):
  file_path: str
  def __init__ (self, file_path: str):
    self.file_path = file_path

  def load (self) -> str:
    with open(self.file_path, "r") as f:
      return json.load(f)
