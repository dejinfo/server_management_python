import psycopg2
#creating database

class Server_manage:
    def create_database(self):
        base = psycopg2.connect(
            host='localhost',
            database ='postgres',
            user='postgres',
            password='tomandjerry',
            port=5432
        )
        base.autocommit = True
        # creating database
        cursor = base.cursor()
        cursor.execute("DROP DATABASE IF EXISTS server_management09")
        cursor.execute("CREATE DATABASE server_management09")
        cursor.close()




s = Server_manage()
s.create_database()
