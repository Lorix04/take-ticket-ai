from typing import List
from langchain_core.tools import tool
from amadeus import Client, ResponseError

# App modules
from config import get_settings
from .locale_tools import translate_to_english
from models import AirportInput, AirportOutput

settings = get_settings()


@tool("lookup_airport", args_schema=AirportInput)
def lookup_airport(city: str) -> List[AirportOutput]:
    """Cerca codici aeroportuali per una città usando Amadeus SDK."""
    if not settings.amadeus_api_key or not settings.amadeus_api_secret:
        return [AirportOutput(code="ERROR", name="Amadeus credentials missing", city="")]

    amadeus = Client(client_id=settings.amadeus_api_key, client_secret=settings.amadeus_api_secret)

    # Normalizza/Traduci il nome città in inglese se necessario
    original_city = (city or "").strip()
    translated_city = translate_to_english(original_city)

    try:
        resp = amadeus.reference_data.locations.get(subType="AIRPORT", keyword=translated_city or original_city)
    except ResponseError as e:
        return [AirportOutput(code="ERROR", name=f"Amadeus error: {e}", city="")]

    airports = getattr(resp, "data", []) or []
    # Fallback per traduzioni comuni (es. "Roma" -> "Rome")
    if not airports:
        synonyms = {
            "roma": "rome", "milano": "milan", "firenze": "florence", "napoli": "naples",
            "venezia": "venice", "torino": "turin", "genova": "genoa", "bologna": "bologna",
        }
        alt = synonyms.get(city.strip().lower())
        if alt:
            try:
                resp = amadeus.reference_data.locations.get(subType="AIRPORT", keyword=alt)
                airports = getattr(resp, "data", []) or []
            except ResponseError:
                pass
    if not airports:
        return [AirportOutput(code="ERROR", name="Nessun aeroporto trovato", city="")]

    # Preferisci risultati coerenti con la città inserita (es. Roma/Rome in Italia)
    city_norm = city.strip().lower()
    preferred_names = {city_norm}
    if city_norm == "roma":
        preferred_names.add("rome")
    if city_norm == "milano":
        preferred_names.add("milan")
    if city_norm == "firenze":
        preferred_names.add("florence")
    if city_norm == "napoli":
        preferred_names.add("naples")
    if city_norm == "venezia":
        preferred_names.add("venice")
    if city_norm == "torino":
        preferred_names.add("turin")

    def matches_city(a: dict) -> bool:
        addr = a.get("address", {})
        city_name = (addr.get("cityName") or "").strip().lower()
        country = (addr.get("countryCode") or "").upper()
        return city_name in preferred_names or (city_norm in {"roma","rome"} and country == "IT")

    # Primo filtro: città coerente E Italia (se Roma/Rome)
    def matches_city_it(a: dict) -> bool:
        addr = a.get("address", {})
        city_name = (addr.get("cityName") or "").strip().lower()
        country = (addr.get("countryCode") or "").upper()
        return city_name in preferred_names and (city_norm not in {"roma","rome"} or country == "IT")

    filtered = [a for a in airports if matches_city_it(a)] or [a for a in airports if matches_city(a)]
    if not filtered:
        # Se abbiamo risultati ma non coerenti, prova anche con sinonimo inglese
        synonyms = {"roma": "rome", "milano": "milan", "firenze": "florence", "napoli": "naples",
                    "venezia": "venice", "torino": "turin"}
        alt = synonyms.get(city_norm)
        if alt:
            try:
                resp = amadeus.reference_data.locations.get(subType="AIRPORT", keyword=alt)
                alt_airports = getattr(resp, "data", []) or []
                alt_filtered = [a for a in alt_airports if matches_city(a)]
                if alt_filtered:
                    airports = alt_filtered
                elif alt_airports:
                    airports = alt_airports
            except ResponseError:
                pass
    else:
        airports = filtered

    # Se la città è Roma/Rome, preferisci risultati in Italia se disponibili
    if city_norm in {"roma", "rome"} and airports:
        it_only = [a for a in airports if (a.get("address", {}).get("countryCode") or "").upper() == "IT"]
        if it_only:
            airports = it_only

    results: List[AirportOutput] = []
    for airport in airports[:5]:
        code = airport.get("iataCode") or airport.get("id")
        name = airport.get("name", "")
        cityname = airport.get("address", {}).get("cityName", "")
        results.append(AirportOutput(code=code, name=name, city=cityname))

    return results