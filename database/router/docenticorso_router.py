from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Docenti_Corso"
# prefix="/Docenti_Corso" evita di dover ripetere "/Docenti_Corso" nell'URL di ogni rotta
# tags=["Docenti_Corso"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Docenti_Corso", tags=["🧑‍🏫 Docenti Corso 📚"])


# ==========================================
# 1. GET ALL - Recupera tutte le informazioni contenute in Docenti Corso
# ==========================================
@router.get("/GET ALL DOCENTI-CORSO", summary = "Recupera le informazioni di tutte le ID collegate alla correlazione Docenti/Corsi")
def get_DC(conn=Depends(get_database)):
    """
    Recupera l'elenco completo degli id docenti e corso (racchiuse in DocentiCorso) dal database ScuolaDb.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllDC")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Tramite ID recupera le informazioni di correlazione Docenti/Corso
# ==========================================
@router.get("/GET DOCENTI-CORSO BY ID", summary = "Recupera le informazioni di una singolo ID in DocentiCorso")
def get_DCID(dc_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un singolo ID in DocentiCorso passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'dc_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetDCByID ?", [dc_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "ID non trovato"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. POST - Inserisce una nuova informazione collegata al Docente e Corso
# ==========================================
@router.post("/ADD DOCENTI-CORSO", summary = "Inserisce le informazioni di un nuovo collegamento docenti e id")
def add_DC(
        docenti_id: int,
        corso_id: int,
        conn=Depends(get_database)):
    """
    Riceve i dati degli ID e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertDC ?, ?",
                   docenti_id,
                   corso_id
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni dei Docenti e dei Corsi correlati sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina tramite l' ID le informazioni la correlazione tra docenti e corso
# ==========================================
@router.delete("/DELETE DOCENTI CORSO", summary = "Elimina le informazioni di correlazione docenti e id")
def delete_dc(dc_id: int, conn=Depends(get_database)):
    """
    Elimina una correlazione Docente e Corso dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteDC ?", dc_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"La correlazione Docente/Corsso con ID: {dc_id} è stata eliminata con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di una correlazione Docenti/Corso tramite id
# ==========================================
@router.put("/UPDATE DOCENTI-CORSO BY ID", summary = "Aggiorna le informazioni di una correlazione Docente/Corso tramite ID")
def update_dc(
        dc_id: int,
        docente_id: int = None,
        corso_id: int = None,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di una correlazione Docente/Corso esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateDCById ?, ?, ?",
                    dc_id,
                    docente_id,
                    corso_id
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni della correlazione Docenti/Corso sono state aggiornate con successo"}