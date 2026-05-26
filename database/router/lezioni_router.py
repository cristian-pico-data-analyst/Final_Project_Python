from datetime import date
from datetime import time
from fastapi import APIRouter, Depends

from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Lezioni"
# prefix="/Lezioni" evita di dover ripetere "/Lezioni" nell'URL di ogni rotta
# tags=["Lezioni"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Lezioni", tags=["📖 Lezioni 📖"])


# ==========================================
# 1. GET ALL - Recupera tutte le lezioni
# ==========================================
@router.get("/GET ALL LEZIONI", summary = "Recupera le informazioni di tutti le informazioni")
def get_lezioni(conn=Depends(get_database)):
    """
    Recupera l'elenco completo delle lezioni dal database.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllLezioni")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera le informazioni di una lezione in base all' ID
# ==========================================
@router.get("/GET LEZIONI BY ID", summary = "Recupera le informazioni di una singola lezione")
def get_lezionibyID(lezioni_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di una singola lezione in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'lezioni_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetLezioniByID ?", [lezioni_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Lezione non trovate"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. POST - Inserisce un nuova lezione
# ==========================================
@router.post("/ADD LEZIONI", summary = "Inserisce le informazioni di una nuova lezione")
def add_lezioni(
        corso_id: int,
        aula_id: int,
        data_lezione: date,
        ora_inizio: time,
        ora_fine: time,
        conn=Depends(get_database)):
    """
    Riceve i dati delle lezioni e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertLezioni ?, ?, ?, ?, ?",
                    corso_id,
                    aula_id,
                    data_lezione,
                    ora_inizio,
                    ora_fine
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni delle lezioni sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina una lezione tramite id
# ==========================================
@router.delete("/DELETE LEZIONI BY ID", summary = "Elimina le informazioni di una lezione")
def delete_lezioni(lezioni_id: int, conn=Depends(get_database)):
    """
    Elimina una lezione dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteLezioni ?", lezioni_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"La lezione con ID: {lezioni_id} è stato eliminato con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di una lezione tramite id
# ==========================================
@router.put("/UPDATE LEZIONI BY ID", summary = "Aggiorna le informazioni di una lezione")
def update_lezioni(
        lezioni_id: int,
        corso_id: int,
        aula_id: int,
        data_lezione: date,
        ora_inizio: time,
        ora_fine: time,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di un corso esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateLezioneById ?, ?, ?, ?, ?, ?",
                   lezioni_id,
                   corso_id,
                   aula_id,
                   data_lezione,
                   ora_inizio,
                   ora_fine
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni delle lezioni sono state aggiornate con successo"}