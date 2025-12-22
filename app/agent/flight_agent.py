from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from config import get_settings
from tools.airport_tools import lookup_airport
from tools.flight_tools import search_flights

settings = get_settings()

def create_flight_agent():
    """Crea e configura l'agente di ricerca voli."""
    
    # Validazione API key
    if not settings.openai_api_key:
        raise ValueError("OpenAI API Key non configurata")
    
    # Inizializza LLM con settings tipizzati
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,  # Supporto per API compatibili (es. Azure)
    )
    
    # System message ottimizzato
    system_message = SystemMessage(
        content="""Sei un esperto assistente di viaggi specializzato in ricerca voli. 
        Usa i tools disponibili per trovare le migliori offerte.
        Fornisci risposte concise ma complete con prezzi e dettagli.
        Quando disponibili, includi anche uno o più link per prenotare/ricercare il volo (es. Kayak, Skyscanner, Google Flights) presi dal campo booking_urls dei risultati.
        Se non trovi voli, suggerisci date alternative o aeroporti vicini."""
    )
    
    # Crea agente con LangChain v1.x
    agent = create_agent(
        model=llm,
        tools=[lookup_airport, search_flights],
        system_prompt=system_message,
    )
    
    return agent

# Cache dell'agente
_flight_agent = None

def get_flight_agent():
    """Get cached agent instance."""
    global _flight_agent
    if _flight_agent is None:
        _flight_agent = create_flight_agent()
    return _flight_agent

def search_flights_conversational(query: str) -> str:
    """Esegui query conversazionale sull'agente."""
    agent = get_flight_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return response["messages"][-1].content