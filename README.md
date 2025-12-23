# take-ticket-ai

Pronto all'uso come **Flight Finder Pro**, questo CLI combina l'ecosistema LangChain/OpenAI con i tool Amadeus per offrire un assistente di viaggio che cerca voli da un terminale in italiano.

## Caratteristiche principali
- Validazione delle chiavi `AMADEUS_API_*` e `OPENAI_API_KEY` prima di eseguire qualsiasi ricerca.
- Interfaccia interattiva basata su `rich` con prompt, tabelle e colori per guidare la ricerca di voli.
- Modalita `--chat` che richiama un agente LangChain dotato dei tool per ricerche aeroportuali e voli, con risposta assistita da GPT (anche per tradurre citta italiane via `locale_tools`).
- Tool `lookup_airport` e `search_flights` basati sulle SDK Amadeus e su modelli Pydantic per serializzare input/output e costruire link diretti a Kayak, Skyscanner e Google Flights.
- Filtro automatico di aeroporti/ricerche con sinonimi (es. Roma <-> Rome) e link di prenotazione nei risultati.

## Prerequisiti
- Python 3.10+ (Pydantic v2 richiede 3.10 o superiore).
- Chiavi API attive per:
  - `AMADEUS_API_KEY` e `AMADEUS_API_SECRET` per le ricerche volo.
  - `OPENAI_API_KEY` (e opzionalmente `OPENAI_MODEL`, `OPENAI_TEMPERATURE`, `OPENAI_BASE_URL`) per il LangChain agent e la traduzione.

## Installazione
1. Clona la repo (gia esistente) e posizionati nella root:
   ```bash
   cd take-ticket-ai
   ```
2. Installa le dipendenze:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Configurazione
Copiando `.env` (non incluso), definisci almeno:
```env
AMADEUS_API_KEY=tuo_id
AMADEUS_API_SECRET=tuo_secret
OPENAI_API_KEY=sk-...
# Opzionali
OPENAI_MODEL=gpt-5-mini
OPENAI_TEMPERATURE=0.3
OPENAI_BASE_URL=https://api.openai.com/v1
```
Pydantic Settings carica automaticamente il file `.env` dalla root del progetto.

## Esecuzione
- Modalita interattiva: `python -m app.main`. La funzione `interactive_search` mostra prompt per origine, destinazione, data, passeggeri e preferenze.
- Modalita conversazionale: `python -m app.main --chat` per dialogare con l'agente LangChain (richiede OpenAI per completare le risposte).

Ogni ricerca valida restituisce le prime 5 offerte con dettagli di segmento, numero di scali, durata e link generati ai siti di prenotazione.

## Struttura del progetto
- `app/main.py`: entry point CLI e validazione delle configurazioni.
- `app/config.py`: `Settings` Pydantic che carica `.env`.
- `app/agent/flight_agent.py`: crea/agisce un agente LangChain con `search_flights` e `lookup_airport`.
- `app/tools`: tool Amadeus (`airport_tools`, `flight_tools`) e helper linguistico (`locale_tools`).
- `app/models`: modelli Pydantic per input/output degli strumenti.
- `app/reader`: utilita di caricamento domande (`questions.txt` in `app/data/`), mantenuta per estensioni future.

## Note
- `locale_tools.translate_to_english` usa un dizionario base e, quando configurato, un LLM OpenAI per lasicarsi guidare nelle traduzioni.
- Tutte le risposte dell'agente contengono almeno un link di prenotazione quando disponibili, consentendo di passare rapidamente alle piattaforme di booking.
