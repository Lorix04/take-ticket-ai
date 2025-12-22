# Esercizio 1 — Classificatore Domande per Materia

Guida rapida per installare e avviare il progetto su Windows (PowerShell).

## Requisiti
- Python 3.11 (consigliato). Con Python 3.14 possono apparire avvisi di compatibilità Pydantic.
- Windows 10/11 con PowerShell.
- Chiave OpenAI valida (variabile `OPENAI_API_KEY`).

## Installazione
Apri PowerShell nella cartella del progetto e poi:

```powershell
# 1) Crea un virtual env
python -m venv .venv

# 2) Attiva l'ambiente
.\.venv\Scripts\Activate.ps1
# Se ricevi un errore di esecuzione script:
# Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 3) Aggiorna pip e installa le dipendenze
python -m pip install --upgrade pip
pip install langchain langchain-openai pydantic pydantic-settings
```

## Configurazione (.env)
Crea un file `.env` nella radice del progetto con i seguenti parametri (esempio):

```dotenv
# OpenAI
OPENAI_API_KEY=la_tua_chiave
OPENAI_MODEL=gpt-5-mini
OPENAI_TEMPERATURE=1
OPENAI_BASE_URL=https://api.openai.com/v1

# Opzionale: percorso Excel per altre funzionalità
EXCEL_PATH=app\data\emails.xlsx
```

Note:
- La temperatura può essere abbassata (es. `0`) per maggiore stabilità.
- Le chiavi extra nel `.env` vengono ignorate se non usate dal codice.

## Avvio del progetto
Con l'ambiente attivo nella cartella del progetto:

```powershell
python .\main.py
```

In alternativa, senza attivare l'ambiente:

```powershell
.\.venv\Scripts\python.exe .\main.py
```

## Cosa fa
- Legge automaticamente le domande da `app/data/questions.txt` (una domanda per riga).
- Classifica ogni domanda in una materia e stampa a console un JSON con `predicted_subject` e `reasoning`.
- Salva anche i risultati in `app/data/results.json`.

## Formato input
File: `app/data/questions.txt`
- Una domanda per riga.
- Esempio:
  ```
  Calcola l'integrale definito di x^2 tra 0 e 1.
  Qual è la derivata di sin(x)?
  Spiega le fasi della fotosintesi clorofilliana.
  ```

## Risultato atteso (esempio)
Output in console simile a:
```json
[
  {
    "id": null,
    "text": "Calcola l'integrale definito di x^2 tra 0 e 1.",
    "predicted_subject": "Matematica",
    "reasoning": "..."
  }
]
```

In aggiunta viene creato/sovrascritto il file `app/data/results.json` con lo stesso contenuto.

## Troubleshooting
- Errore: "manca OPENAI_API_KEY" → verifica `.env` o variabile d'ambiente.
- Problema attivazione venv su PowerShell → esegui `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e riapri PowerShell.
- Timeout/connessione OpenAI → verifica rete/firewall e `OPENAI_BASE_URL`.
- Avvisi Pydantic con Python 3.14 → usa Python 3.11 per evitare warning.

