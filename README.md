# 🏫 Sistema di Gestione Scolastica - API

Questo progetto è un'applicazione backend sviluppata in **Python** utilizzando il framework  **FastAPI** . Fornisce un set completo di API RESTful per gestire le operazioni amministrative e didattiche di una scuola, tra cui la gestione di studenti, docenti, aule, corsi, lezioni e iscrizioni.

Il sistema si interfaccia con un database **SQL Server** locale utilizzando il driver `pyodbc`. Tutta la logica di accesso e modifica dei dati è demandata a **Stored Procedure** (SP) per garantire sicurezza e ottimizzazione delle query.

## 🛠️ Tecnologie Utilizzate

* **Linguaggio:** Python 3.x
* **Framework Web:** FastAPI
* **Database:** Microsoft SQL Server (`ScuolaDb`)
* **Connettore DB:** `pyodbc`

## 📂 Struttura del Progetto

Il codice è organizzato in moduli (router) per facilitare la manutenzione:

* **`database/`**
  * `db.py`: Gestisce la stringa di connessione a SQL Server (`tuo_server\SQLEXPRESS`) e fornisce il generatore di connessioni (Dependency Injection).
* **`routers/`** (Moduli API)
  * `aule_router.py`: Operazioni CRUD per le 🏛️ Aule.
  * `corsi_router.py`: Operazioni CRUD per i 📚 Corsi.
  * `docenti_router.py`: Operazioni CRUD per i 🧑‍🏫 Docenti (inclusa la ricerca per cognome).
  * `studenti_router.py`: Operazioni CRUD per gli 🧑‍🎓 Studenti (inclusa la ricerca per nome).
  * `lezioni_router.py`: Pianificazione e gestione delle 📖 Lezioni (date, orari, aule).
  * `iscrizioni_router.py`: Gestione delle 📑 Iscrizioni degli studenti ai corsi.
  * `docenticorso_router.py`: Tabella di correlazione per assegnare i 🧑‍🏫 Docenti ai 📚 Corsi.

## 🚀 Funzionalità Principali (Endpoints)

Tutti i moduli implementano i metodi HTTP standard attraverso chiamate a specifiche Stored Procedure.

* **GET ALL:** Recupera tutti i record di una specifica entità (es. `sp_GetAllStudenti`, `sp_GetAllCorsi`).
* **GET BY ID / NAME:** Recupera dettagli specifici di un singolo record passando l'ID o altri parametri di ricerca come nome/cognome.
* **POST (ADD):** Inserisce un nuovo record nel database (es. `sp_InsertIscrizione`).
* **PUT (UPDATE):** Aggiorna parzialmente o totalmente i dati di un record esistente (es. `sp_UpdateDocentiById`).
* **DELETE:** Rimuove fisicamente un record dal database (es. `sp_DeleteAule`).

## ⚙️ Configurazione e Installazione

**1. Clona la repository**

**Bash**

```
gh repo clone cristian-pico-data-analyst/Final_Project_Python
cd <Final_Project_Python>
```

**2. Crea un ambiente virtuale e installa le dipendenze**
Assicurati di avere un file `requirements.txt` con le seguenti librerie, o installale manualmente:

**Bash**

```
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install fastapi uvicorn pyodbc
```

*Nota: Assicurati di avere i driver ODBC di SQL Server installati sulla tua macchina (ODBC Driver 17 for SQL Server).*

**3. Configura il Database**
Nel file `db.py`, verifica che la stringa di connessione corrisponda all'istanza del tuo SQL Server locale:

**Python**

```
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tuo_server\\SQLEXPRESS;"
    "DATABASE=ScuolaDb;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
```

Assicurati che il database `ScuolaDb` e tutte le Stored Procedure (es. `sp_GetAllStudenti`, `sp_InsertCorso`, ecc.) siano state correttamente create in SQL Server.

**4. Avvia il server locale**
Presumendo che tu abbia un file principale (es. `app.py`) che include tutti questi router, avvia l'applicazione con Uvicorn:

**Bash**

```
uvicorn app:app --reload
```

## 📖 Documentazione API

FastAPI genera automaticamente una documentazione interattiva. Una volta avviato il server, puoi esplorare e testare tutti gli endpoint direttamente dal tuo browser:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`
