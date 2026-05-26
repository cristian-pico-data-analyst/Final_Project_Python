from datetime import date  # Modulo standard di Python per gestire le date (riconosciuto da Swagger)
from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Docenti"
# prefix="/Docenti" evita di dover ripetere "/Docenti" nell'URL di ogni rotta
# tags=["Docenti"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Docenti", tags=["🧑‍🏫 Docenti 🧑‍🏫"])


# ==========================================
# 1. GET ALL - Recupera tutti i Docenti
# ==========================================
@router.get("/GET ALL DOCENTI", summary="Recupera le informazioni di tutti i docenti")
def get_docenti(conn=Depends(get_database)):
    """
    Recupera l'elenco completo degli studenti dal database.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllDocenti")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera un singolo docente attraverso ID
# ==========================================
@router.get("/GET DOCENTI BY ID", summary="Recupera un singolo docente tramite ID")
def get_docentebyID(docente_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un singolo docente in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'docente_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetDocentiByID ?", [docente_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Docente non trovato"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. GET BY NAME - Recupera i docenti in base al cognome
# ==========================================
@router.get("/GET DOCENTI BY SURNAME", summary="Ricerca le informazioni di un docente tramite cognome")
def get_docentebysurname(docente_surname: str, conn=Depends(get_database)):
    """
    Recupera i dati di un singolo docente in base al cognome passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'docente_surname' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetDocenteBySurname ?", docente_surname)
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che il nome non esiste nel database
    if not rows:
        return {"Messaggio": f"Il docente {docente_surname} non è stato trovato"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    risultato = [dict(zip(column, row)) for row in rows]
    return {"Messaggio": "Docente trovato con successo", "Dati": risultato}


# ==========================================
# 4. POST - Inserisce un nuovo docente
# ==========================================
@router.post("/ADD DOCENTE", summary = "Inserisce un nuovo docente")
def add_docente(
        docente_id: int,
        nome: str,
        cognome: str,
        email: str = None,  # Parametro opzionale (default None)
        specializzazione: str = None,  # Parametro opzionale
        conn=Depends(get_database)):
    """
    Riceve i dati del docente e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertDocente ?, ?, ?, ?, ?",
                   docente_id,
                   nome,
                   cognome,
                   email,
                   specializzazione
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni del docente sono state inserite con successo"}


# ==========================================
# 5. DELETE - Elimina un docente tramite ID
# ==========================================
@router.delete("/DELETE DOCENTE BY ID", summary="Elimina le informazioni di un docente")
def delete_studenti(docente_id: int, conn=Depends(get_database)):
    """
    Elimina uno docente dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteDocente ?", docente_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"Il docente {docente_id} è stato eliminato con successo"}


# ==========================================
# 6. PUT - Aggiorna i dati di un docente
# ==========================================
@router.put("/UPDATE DOCENTE BY ID", summary = "Aggiorna le informazioni di un docente")
def update_docente(
        docente_id: int,
        nome: str,
        cognome: str,
        email: str = None,  # Parametro opzionale (default None)
        specializzazione: str = None,  # Parametro opzionale
        conn=Depends(get_database)):
    """
    Aggiorna i dati di uno docente esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateDocentiById ?, ?, ?, ?, ?, ?, ?",
                   docente_id,
                   nome,
                   cognome,
                   email,
                   specializzazione
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni del docente sono state aggiornate con successo"}