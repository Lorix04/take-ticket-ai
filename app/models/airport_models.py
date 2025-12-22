from pydantic import BaseModel, Field
from typing import List

class AirportInput(BaseModel):
    """Input per la ricerca aeroporti."""
    city: str = Field(description="Nome della città per cercare l'aeroporto")

class AirportOutput(BaseModel):
    """Output della ricerca aeroporti."""
    code: str
    name: str
    city: str


class QuestionCreate(BaseModel):
    """Modello per domande caricate da file."""
    text: str
    id: str