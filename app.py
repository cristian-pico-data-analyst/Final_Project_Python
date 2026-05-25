from fastapi import FastAPI, Depends
from database.db import get_database
from database.router.studenti_router import router as studenti_router
from database.router.corsi_router import router as corsi_router

#from router.Studenti_routers import router as studenti_routers
#from router.Corsi_routers import router as corsi_routers

app = FastAPI(title="Gestione Registro Studenti")
app.include_router(studenti_router)
app.include_router(corsi_router)

@app.get("/", tags=["Gestione Registro Studenti"])
def lista_tabella(connection = Depends(get_database)):
    cursor = connection.cursor()

    cursor.execute("EXEC sp_ListaTabelle")
    tabelle = [row[0] for row in cursor.fetchall()]

    connection.close()

    return tabelle

@app.get("/tabella/{nome_tabella}")
def leggi_tabella(nome_tabella: str, conn = Depends(get_database)):

    cursor = conn.cursor()

    query = f"SELECT * FROM [{nome_tabella}]"
    cursor.execute(query)

    column = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    risultati = [dict(zip(column, row)) for row in rows]

    return risultati
