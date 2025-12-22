from typing import List
from langchain_core.tools import tool
from amadeus import Client, ResponseError
from config import get_settings
from models import FlightSearchInput, FlightOffer, FlightSegment

settings = get_settings()


@tool("search_flights", args_schema=FlightSearchInput)
def search_flights(
    origin: str, destination: str, departure_date: str,
    adults: int = 1, non_stop: bool = False
) -> List[FlightOffer]:
    """Cerca le offerte volo usando Amadeus SDK."""
    if not settings.amadeus_api_key or not settings.amadeus_api_secret:
        return [FlightOffer(price="ERROR", airline="", duration="", stops=0, segments=[])]

    amadeus = Client(client_id=settings.amadeus_api_key, client_secret=settings.amadeus_api_secret)

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "nonStop": str(non_stop).lower(),
        "max": "20",
        "currencyCode": "EUR",
    }

    try:
        resp = amadeus.shopping.flight_offers_search.get(**params)
    except ResponseError as e:
        return [FlightOffer(price=f"ERROR: {e}", airline="", duration="", stops=0, segments=[])]

    data = getattr(resp, "data", []) or []
    if not data:
        return [FlightOffer(price="0 EUR", airline="", duration="", stops=0, segments=[])]

    offers = []
    for offer in data[:5]:
        itineraries = offer.get("itineraries", [])
        first_it = itineraries[0] if itineraries else {}
        segments = first_it.get("segments", [])
        stops = max(0, len(segments) - 1)
        airline = segments[0].get("carrierCode") if segments else ""
        price = offer.get("price", {}).get("total", "0")
        flight_segments = []
        for seg in segments:
            flight_segments.append(FlightSegment(
                flight_number=f"{seg.get('carrierCode','')}{seg.get('number','')}",
                departure=seg.get("departure", {}).get("iataCode", ""),
                arrival=seg.get("arrival", {}).get("iataCode", ""),
                departure_time=seg.get("departure", {}).get("at", ""),
                arrival_time=seg.get("arrival", {}).get("at", ""),
            ))

        # Build simple booking/search deep links (Kayak, Skyscanner, Google Flights)
        try:
            orig = flight_segments[0].departure if flight_segments else params["originLocationCode"]
            dest = flight_segments[-1].arrival if flight_segments else params["destinationLocationCode"]
        except Exception:
            orig = params["originLocationCode"]
            dest = params["destinationLocationCode"]

        dep_date = params["departureDate"]  # YYYY-MM-DD
        y, m, d = dep_date.split("-")
        # Skyscanner expects ddmmyy
        skyscanner_date = f"{d}{m}{y[-2:]}"
        adults = int(params.get("adults", 1))
        direct_only = (stops == 0)
        kayak_filters = "&fs=stops=0" if direct_only else ""
        booking_urls = {
            "kayak": f"https://www.kayak.com/flights/{orig}-{dest}/{dep_date}?adults={adults}{kayak_filters}",
            "skyscanner": f"https://www.skyscanner.net/transport/flights/{orig.lower()}/{dest.lower()}/{skyscanner_date}/?adults={adults}&directOnly={'true' if direct_only else 'false'}&currency=EUR",
            "google_flights": f"https://www.google.com/travel/flights?hl=en&q=Flights%20from%20{orig}%20to%20{dest}%20on%20{dep_date}",
        }

        offers.append(FlightOffer(
            price=f"{price} EUR",
            airline=airline,
            duration=first_it.get("duration", ""),
            stops=stops,
            segments=flight_segments,
            booking_urls=booking_urls,
        ))

    return offers