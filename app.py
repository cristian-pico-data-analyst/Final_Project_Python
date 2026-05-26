# =====================================================================
# 1. IMPORT DELLE LIBRERIE E DEI MODULI
# =====================================================================
from fastapi import FastAPI, Depends
from database.db import get_database

# Importazione dei router
# Ogni router gestisce le API relative a una specifica entità scolastica
from database.router.studenti_router import router as studenti_router
from database.router.corsi_router import router as corsi_router
from database.router.docenti_router import router as docenti_router
from database.router.iscrizioni_router import router as iscrizioni_router
from database.router.aule_router import router as aule_router
from database.router.docenticorso_router import router as docenticorso_router
from database.router.lezioni_router import router as lezioni_router

# =====================================================================
# 2. INIZIALIZZAZIONE DELL'APP E INCLUSIONE DEI ROUTER
# =====================================================================

# Creazione dell'istanza principale di FastAPI con un titolo descrittivo
app = FastAPI(title="Gestione Registro Database Scolastico")

# Aggancio di tutti i router all'applicazione principale.
# Questo rende il codice modulare, evitando di avere tutte le rotte in questo file.
app.include_router(studenti_router)
app.include_router(corsi_router)
app.include_router(docenti_router)
app.include_router(iscrizioni_router)
app.include_router(aule_router)
app.include_router(docenticorso_router)
app.include_router(lezioni_router)


# =====================================================================
# 3. ENDPOINT GENERICI (ROOT E LETTURA DINAMICA)
# =====================================================================

# ---------------------------------------------------------------------
# Endpoint: Lista delle tabelle (Root "/")
# ---------------------------------------------------------------------
@app.get("/", tags=["Gestione Registro Studenti"])
def lista_tabella(connection=Depends(get_database)):
    """
    Ritorna la lista di tutte le tabelle presenti nel database 
    sfruttando la Stored Procedure 'sp_ListaTabelle'.
    """
    # Apre il cursore per eseguire i comandi SQL
    cursor = connection.cursor()

    # Esegue la Stored Procedure
    cursor.execute("EXEC sp_ListaTabelle")

    # Estrae solo i nomi delle tabelle dalla tupla dei risultati
    tabelle = [row[0] for row in cursor.fetchall()]

    # Chiude la connessione per liberare risorse
    connection.close()

    return tabelle


# ---------------------------------------------------------------------
# Endpoint: Lettura dinamica di una specifica tabella
# ---------------------------------------------------------------------
@app.get("/tabella/{nome_tabella}")
def leggi_tabella(nome_tabella: str, conn=Depends(get_database)):
    """
    Data una specifica tabella in input nell'URL, 
    recupera e restituisce tutti i suoi record.
    """
    cursor = conn.cursor()

    # Compone la query dinamicamente in base al nome passato nell'URL
    query = f"SELECT * FROM [{nome_tabella}]"
    cursor.execute(query)

    # Estrae dinamicamente i nomi delle colonne dal cursore
    column = [col[0] for col in cursor.description]

    # Recupera tutti i dati (le righe)
    rows = cursor.fetchall()

    conn.close()

    # Unisce i nomi delle colonne con i valori delle righe per creare 
    # una lista di dizionari, perfetta per una risposta JSON in FastAPI.
    risultati = [dict(zip(column, row)) for row in rows]

    return risultati