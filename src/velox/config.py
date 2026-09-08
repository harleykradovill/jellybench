from pathlib import Path
import yaml
from pydantic import BaseModel, Field

CONFIG_PATH = Path("configuration.yaml")


class ServerConfig(BaseModel):
    url: str = Field(
        default="http://localhost:8096", description="Jellyfin server base URL"
    )
    api_key: str = Field(default="", description="Jellyfin API key")


class Config(BaseModel):
    server: ServerConfig = ServerConfig()

    @classmethod
    def load(cls, path: Path = CONFIG_PATH) -> "Config":
        if path.exists():
            return cls.model_validate(yaml.safe_load(path.read_text()))
        return cls()

    def save(self, path: Path = CONFIG_PATH) -> None:
        path.write_text(yaml.safe_dump(self.model_dump(), sort_keys=False))
