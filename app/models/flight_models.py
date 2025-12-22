from pydantic import BaseModel, Field
from typing import List, Dict

class FlightSearchInput(BaseModel):
    """Input per la ricerca voli."""
    origin: str = Field(description="Codice IATA aeroporto di partenza")
    destination: str = Field(description="Codice IATA aeroporto di destinazione")
    departure_date: str = Field(description="Data di partenza in formato YYYY-MM-DD")
    adults: int = Field(default=1, ge=1, le=9, description="Numero di passeggeri")
    non_stop: bool = Field(default=False, description="True per voli diretti")

class FlightSegment(BaseModel):
    """Singolo segmento di volo (tratta)."""
    flight_number: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str

class FlightOffer(BaseModel):
    """Offerta volo completa."""
    price: str
    airline: str
    duration: str
    stops: int
    segments: List[FlightSegment]
    booking_urls: Dict[str, str] = Field(default_factory=dict, description="Deep links to book/search this itinerary")