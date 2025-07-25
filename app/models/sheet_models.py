"""
Modelos de dados para integração com Google Sheets.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator


class SheetInput(BaseModel):
    """Modelo para entrada de dados na planilha."""
    name: str = Field(..., min_length=2, max_length=100)
    serie: int = Field(..., gt=0)
    initial_weight: str = Field(..., pattern=r'^\d+(\.\d+)?kg$')
    date: str
    
    @validator('date')
    def validate_date_format(cls, v):
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Data deve estar no formato YYYY-MM-DD')
    
    @validator('name')
    def validate_name(cls, v):
        return ' '.join(word.capitalize() for word in v.strip().split())
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "serie": 3,
                "initial_weight": "75kg",
                "date": "2024-01-15"
            }
        }


class SheetResponse(BaseModel):
    """Modelo para resposta da API."""
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None


class SheetRecord(BaseModel):
    """Modelo para um registro da planilha."""
    name: str
    serie: int
    initial_weight: str
    date: str
