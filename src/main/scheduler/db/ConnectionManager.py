import pymssql
import os

class ConnectionManager:
    self.server_name = os.getenv("Server")
    self.user = os.getenv("UserID")
    self.db_name = os.getenv("DBName")
    self.password = os.getenv("Password")
    self.conn = None

    def create_connection(self):
        try:
            self.conn = pymssql.connect(server=self.server_name, user=self.user, password=self.Password, database=self.db_name)
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            sqlrc = str(db_err.args[0])
            print("Exception code: " + str(sqlrc))
            if len(db_err) > 1:
                print("Exception message: " + db_err.args[1])
        return conn

    def close_connection(self):
        try:
            self.conn.close()
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            sqlrc = str(db_err.args[0])
            print("Exception code: " + str(sqlrc))
            if len(db_err) > 1:
                print("Exception message: " + db_err.args[1])
