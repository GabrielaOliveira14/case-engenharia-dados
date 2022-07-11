def handleQueryExecute(connect, query):
    cursor = connect.cursor()
    cursor.execute(query)
    connect.commit()