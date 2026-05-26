from fastapi import APIRouter, Depends
from database.db import get_database  # La funzione che gestisce la connessione al DB

# Inizializzazione del Router per la risorsa "Aule"
# prefix="/Aule" evita di dover ripetere "/Aule" nell'URL di ogni rotta
# tags=["Aule"] raggruppa queste rotte insieme nella documentazione Swagger (/docs)
router = APIRouter(prefix="/Aule", tags=["🏛️ Aule 🏛️"])


# ==========================================
# 1. GET ALL - Recupera tutti le aule
# ==========================================
@router.get("/", summary = "Recupera le informazioni di tutti le aule")
def get_aule(conn=Depends(get_database)):
    """
    Recupera l'elenco completo delle aule dal database ScuolaDb.
    Usiamo Depends(get_database) per iniettare la connessione attiva.
    """
    cursor = conn.cursor()

    # Esecuzione della Stored Procedure per leggere tutti i record
    cursor.execute("EXEC sp_GetAllAule")
    rows = cursor.fetchall()  # Recupera tutte le righe restituite

    # Estrae i nomi delle colonne dal cursore per mappare i dati in un dizionario
    column = [col[0] for col in cursor.description]

    # Converte la lista di tuple in una lista di dizionari {colonna: valore}
    return [dict(zip(column, row)) for row in rows]


# ==========================================
# 2. GET BY ID - Recupera una singola aula
# ==========================================
@router.get("/{aule_id}", summary = "Recupera le informazioni di una singola aula tramite ID")
def get_aulebyID(aule_id: int, conn=Depends(get_database)):
    """
    Recupera i dati di un singola aula in base all'ID passato nell'URL.
    """
    cursor = conn.cursor()

    # Passiamo 'aule_id' corretto alla Stored Procedure
    cursor.execute("EXEC sp_GetAuleByID ?", [aule_id])
    rows = cursor.fetchall()

    # Se la lista è vuota, significa che l'ID non esiste nel database
    if not rows:
        return {"Messaggio": "Aula non trovata"}

    # Se esiste, mappa il risultato in un dizionario e lo restituisce
    column = [col[0] for col in cursor.description]
    return [dict(zip(column, row)) for row in rows]

# ==========================================
# 3. POST - Inserisce una nuova aula
# ==========================================
@router.post("/ADD_Aula", summary = "Inserisce le informazioni di una nuova aula")
def add_aula(
        nome_aula: str,
        capacita: str,
        conn=Depends(get_database)):
    """
    Riceve i dati delle aule e invoca la SP di inserimento.
    """
    cursor = conn.cursor()

    # Esegue la SP passando tutti i parametri posizionali (?) in ordine sicuro
    cursor.execute("EXEC sp_InsertCorso ?, ?",
                   nome_aula,
                   capacita
                   )

    # IMPORTANTE: Salva le modifiche nel database (essendo una query di scrittura)
    conn.commit()

    return {"Messaggio": "Le informazioni dell' aula sono state inserite con successo"}


# ==========================================
# 4. DELETE - Elimina un' aula tramite id
# ==========================================
@router.delete("/Delete/{aula_id}", summary = "Elimina le informazioni di un' aula")
def delete_aula(aula_id: int, conn=Depends(get_database)):
    """
    Elimina un' aula dal database tramite il suo ID.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure passando solo l'ID necessario alla cancellazione
    cursor.execute("EXEC sp_DeleteAule ?", aula_id)

    # Conferma l'eliminazione sul database
    conn.commit()

    return {"Messaggio": f"L'aula con ID: {aula_id} è stato eliminato con successo"}


# ==========================================
# 5. PUT - Aggiorna i dati di un' aula tramite id
# ==========================================
@router.put("/Update/{aula_id}", summary = "Aggiorna le informazioni di un' aula tramite ID")
def update_aule(
        aula_id: int,
        nome_aula: str = None,
        capacita: str = None,
        conn=Depends(get_database)):
    """
    Aggiorna i dati di un' aula esistente usando il metodo HTTP PUT.
    """
    cursor = conn.cursor()

    # Esegue la stored procedure di aggiornamento inviando i nuovi dati
    cursor.execute("EXEC sp_UpdateAuleById ?, ?, ?",
                    aula_id,
                    nome_aula,
                    capacita
                   )

    # Conferma le modifiche dell'aggiornamento
    conn.commit()

    return {"Messaggio": "Le informazioni dell' aula sono state aggiornate con successo"}