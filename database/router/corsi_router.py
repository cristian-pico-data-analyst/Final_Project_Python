from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Corsi"
# prefix="/Corsi" evita di dover ripetere "/Corsi" nell'URL di ogni rotta
# tags=["Corsi"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Corsi", tags=["📚 Corsi 📚"])


# ==========================================
# 1. GET ALL - Recupera tutti i corsi
# ==========================================
@router.get("/GET ALL CORSI", summary = "Recupera le informazioni di tutti gli studenti")
def get_corsi(conn=Depends(get_database)):
    """
    Recupera l'elenco completo dei corsi dal database.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllCorsi")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera un singolo corso
# ==========================================
@router.get("/GET CORSI BY ID", summary = "Recupera le informazioni di un singolo corso")
def get_corsibyID(corsi_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un singolo corso in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'corso_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetCorsiByID ?", [corsi_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Corso non trovato"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. POST - Inserisce un nuovo corso
# ==========================================
@router.post("/ADD CORSI", summary = "Inserisce le informazioni di un nuovo corso")
def add_corsi(
        nome_corso: str,
        descrizione_corso: str,
        crediti: int = None,
        durata: int = None,
        conn=Depends(get_database)):
    """
    Riceve i dati deli corsi e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertCorso ?, ?, ?, ?",
                   nome_corso,
                   descrizione_corso,
                   crediti,
                   durata
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni del corso sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina un corso tramite id
# ==========================================
@router.delete("/DELETE CORSI BY ID", summary = "Elimina le informazioni di un corso")
def delete_corsi(corsi_id: int, conn=Depends(get_database)):
    """
    Elimina un corso dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteCorsi ?", corsi_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"Il corso con ID:{corsi_id} è stato eliminato con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di un corso tramite ID
# ==========================================
@router.put("/UPDATE CORSI BY ID", summary = "Aggiorna le informazioni di un corso")
def update_corsi(
        corso_id: int,
        nome_corso: str = None,
        descrizione_corso: str = None,
        crediti: str = None,
        durata: str = None,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di un corso esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateCorsoById ?, ?, ?, ?, ?",
                    corso_id,
                    nome_corso,
                    descrizione_corso,
                    crediti,
                    durata
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni del corso sono state aggiornate con successo"}