from datetime import date
from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Iscrizioni"
# prefix="/Iscrizioni" evita di dover ripetere "/Corsi" nell'URL di ogni rotta
# tags=["Iscrizioni"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Iscrizioni", tags=["📑 Iscrizioni 📑"])


# ==========================================
# 1. GET ALL - Recupera tutti le iscrizioni
# ==========================================
@router.get("/GET ALL ISCRIZIONI", summary = "Recupera le informazioni di tutte le iscrizioni")
def get_iscrizioni(conn=Depends(get_database)):
    """
    Recupera l'elenco completo delle iscrizioni dal database.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllIscrizioni")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera una singola iscrizione
# ==========================================
@router.get("/GET ISCRIZIONE BY ID", summary="Recupera le informazioni di una singola iscrizione")
def get_iscrizionibyID(iscrizioni_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un'iscrizione in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'iscrizione_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetIscrizioniByID ?", [iscrizioni_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Iscrizione non presente"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. POST - Inserisce una nuova iscrizione
# ==========================================
@router.post("/ADD ISCRIZIONI",
            summary="Crea una nuova iscrizione nel registro", # Il testo in grassetto accanto al bottone POST
            description="Questa rotta permette di iscrivere uno studente a un corso. **Attenzione:** verifica che l'ID studente e l'ID corso esistano prima di procedere.", # Il testo testeso dentro il bottone
            response_description="Ritorna un messaggio di successo o di errore", # Descrizione della risposta in basso
            deprecated=False # Se lo imposti su True, il bottone apparirà barrato in grigio (utile per le vecchie API)
             )
def add_iscrizione(
        studente_id: int,
        corso_id: int,
        data_iscrizione: date = None,
        conn=Depends(get_database)):
    """
    Riceve i dati dello studente e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertIscrizione ?, ?, ?",
                   studente_id,
                   corso_id,
                   data_iscrizione
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni dell'iscrizione sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina un' iscrizione tramite id
# ==========================================
@router.delete("/DELETE ISCRIZIONE BY ID", summary = "Elimina le informazioni di un'iscrizione tramite il suo ID")
def delete_iscrizioni(iscrizioni_id: int, conn=Depends(get_database)):
    """
    Elimina un' iscrizione dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteIscrizione ?", iscrizioni_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"L'iscrizione {iscrizioni_id} è stato eliminato con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di un' iscrizione tramite id
# ==========================================
@router.put("/UPDATE LEZIONE BY ID", summary="Aggiorna i dati di un'iscrizione tramite ID")
def update_iscrizione(
        iscrizione_id: int,
        studente_id: int,
        corso_id: int,
        data_iscrizione: date = None,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di un'iscrizione esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateIscrizioniById ?, ?, ?, ?",
                    iscrizione_id,
                    studente_id,
                    corso_id,
                    data_iscrizione
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni dell'iscrizione sono state aggiornate con successo"}