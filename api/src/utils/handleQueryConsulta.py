import sqlite3


def handleQueryConsulta(query, dbName):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(query)
    consulta = cursor.fetchall()
    conn.close()
    return consulta
