import mysql.connector


config = {
    'user': 'maistro',
    'password': 'maistropassword',
    'host': 'semi1albumpro.c3o826gqmko6.us-east-2.rds.amazonaws.com',
    'database': 'albumpro',
    'port':'3306',
    'raise_on_warnings': True,
}

# cnx = mysql.connector.connect(**config)
def execute_query(query, params= None):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        if params is None:
            cursor.execute(query)
            print("ENTRO 1", )
        else:
            print(cursor.execute(query, params))
            
            print("ENTRO 2", )
        if cursor.with_rows:
            print("ENTRO 3", )
            return cursor.fetchall()
        else:
            connection.commit()
            cursor.close()
            connection.close()        
            print("ENTRO TRY DB ", )
            return [True, cursor.lastrowid]
    except Exception as e:
        print("ENTRO EXCEPT ", e)
        return False