"""
Configurações da aplicação usando variáveis de ambiente.
"""
import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):    
    google_credentials_path: str = "credentials/service-account.json"
    sheet_name: str = "Academia"
    
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    allowed_origins: str = "*"
    
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_credentials_path(self) -> Path:
        """Retorna o caminho absoluto para as credenciais."""
        return Path(self.google_credentials_path).resolve()
    
    def get_allowed_origins(self) -> List[str]:
        """Processa a string de origens permitidas para uma lista."""
        if self.allowed_origins == "*":
            return ["*"]
        
        origins = [origin.strip() for origin in self.allowed_origins.split(",")]
        return [origin for origin in origins if origin]


settings = Settings() 