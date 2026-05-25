from datetime import date  # Modulo standard di Python per gestire le date (riconosciuto da Swagger)
from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Studenti"
# prefix="/Studenti" evita di dover ripetere "/Studenti" nell'URL di ogni rotta
# tags=["Studenti"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Studenti", tags=["Studenti"])


# ==========================================
# 1. GET ALL - Recupera tutti gli studenti
# ==========================================
@router.get("/")
def get_studenti(conn=Depends(get_database)):
    """
    Recupera l'elenco completo degli studenti dal database.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllStudenti")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera un singolo studente
# ==========================================
@router.get("/{studente_id}")
def get_studentibyID(studente_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un singolo studente in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'studente_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetStudenteByID ?", [studente_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Studente non trovato"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 3. POST - Inserisce un nuovo studente
# ==========================================
@router.post("/ADD_Studenti")
def add_studenti(
        studente_id: int,
        nome: str,
        cognome: str,
        data_nascita: date = None,  # Accetta una data in formato YYYY-MM-DD
        email: str = None,  # Parametro opzionale (default None)
        telefono: str = None,  # Parametro opzionale
        codice_fiscale: str = None,  # Parametro opzionale
        conn=Depends(get_database)):
    """
    Riceve i dati dello studente e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertStudente ?, ?, ?, ?, ?, ?, ?",
                   studente_id,
                   nome,
                   cognome,
                   data_nascita,
                   email,
                   telefono,
                   codice_fiscale
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni dello studente sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina uno studente
# ==========================================
@router.delete("/Delete/{studente_id}")
def delete_studenti(studente_id: int, conn=Depends(get_database)):
    """
    Elimina uno studente dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteStudente ?", studente_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"Lo studente {studente_id} è stato eliminato con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di uno studente
# ==========================================
@router.put("/Update/{studente_id}")
def update_studenti(
        studente_id: int,
        nome: str,
        cognome: str,
        data_nascita: date = None,
        email: str = None,
        telefono: str = None,
        codice_fiscale: str = None,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di uno studente esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateStudenteById ?, ?, ?, ?, ?, ?, ?",
                   studente_id,
                   nome,
                   cognome,
                   data_nascita,
                   email,
                   telefono,
                   codice_fiscale
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni dello studente sono state aggiornate con successo"}