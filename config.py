import yaml
from pydantic import BaseModel

class SQLiteConfig(BaseModel):
    path: str

class JSONConfig(BaseModel):
    base_dir: str
    mode: str

class StorageConfig(BaseModel):
    primary: str
    secondary: str

class Config(BaseModel):
    storage: StorageConfig
    sqlite: SQLiteConfig
    json: JSONConfig

def load_config(file_path: str) -> Config:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return Config(**data)

# Example usage:
# config = load_config("config.yaml")
# print(config.storage.primary)
