from agent.flight_agent import search_flights_conversational, get_flight_agent
from tools.airport_tools import lookup_airport
from tools.flight_tools import search_flights
from config import get_settings
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
import sys

console = Console()
settings = get_settings()

def validate_config():
    """Valida che tutte le configurazioni necessarie siano presenti."""
    errors = []
    
    if not settings.amadeus_api_key:
        errors.append("AMADEUS_API_KEY mancante")
    if not settings.amadeus_api_secret:
        errors.append("AMADEUS_API_SECRET mancante")
    if not settings.openai_api_key:
        errors.append("OPENAI_API_KEY mancante")
    
    if errors:
        console.print("[red]❌ Configurazione incompleta:[/red]")
        for error in errors:
            console.print(f"  - {error}")
        console.print("\n[yellow]Assicurati di aver configurato il file .env[/yellow]")
        sys.exit(1)
    
    console.print("[green]✅ Configurazione valida![/green]")

def interactive_search():
    """Interfaccia interattiva migliorata."""
    validate_config()
    
    console.print("\n🛫 [bold cyan]FLIGHT FINDER PRO v1.0[/bold cyan]", justify="center")
    console.print("=" * 50)
    
    # ... (resto del codice rimane uguale al precedente)

def chat_mode():
    """Modalità conversazionale."""
    validate_config()
    console.print("\n[bold green]🤖 Modalità Chat - Digita 'exit' per uscire[/bold green]")
    
    while True:
        query = Prompt.ask("\n[bold]Tu[/bold]")
        if query.lower() in ["exit", "quit", "esci"]:
            break
        
        try:
            response = search_flights_conversational(query)
            console.print(f"[bold blue]Agente:[/bold blue] {response}")
        except Exception as e:
            console.print(f"[red]Errore: {e}[/red]")

if __name__ == "__main__":
    validate_config()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--chat":
        chat_mode()
    else:
        interactive_search()