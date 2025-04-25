import pyodbc

class Database:
    def __init__(self):
        self.server = 'DESKTOP-N4J2UNJ'
        self.database = 'Traffic_Crashes'
        self.driver = '{ODBC Driver 17 for SQL Server}'  # Adjust based on your installed driver
        self.conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
    
    def get_connection(self):
        return pyodbc.connect(self.conn_str)
    
    def execute_query(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()