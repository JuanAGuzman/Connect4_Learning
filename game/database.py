import sqlite3 as sql
import os

class DataBase:
    TABLES = [{"name": "sarsa",
               "columns": ["state CHAR(42)", "action TINYINT", "reward FLOAT"]},
               {"name": "qlearning",
                "columns": ["state CHAR(42)", "action TINYINT", "reward FLOAT"]}
                ]
                
    def __init__(self, name):
        """
        Database class init function creating a connection to de database
        and a cursor item.

        Parameters:
            - name (str):
                Filename of the database
        """

        self.name = name
        self.connection = sql.connect(name)
        self.cursor = self.connection.cursor()

        if not self.get_tables():
            for table in self.TABLES:
                self.create_table(table)

    def query(self, query):
        """
        Query function designed to easy execute a single
        SQL statement calling through the cursor item.

        Parameters:
            - query (str):
                Query in sql language

        Returns:
            - The result of the consulted        
        """

        result = self.cursor.execute(query)
        return result
    
    def commit(self):
        """
        
        """

        self.connection.commit()

    def get_tables(self):
        """
        Get tables
        """

        query = f"""
                SELECT name FROM sqlite_master  
                WHERE type='table'
                ;
                """
        
        tables = self.query(query).fetchall()
        return tables
    
    def create_table(self, table):
        """
        
        """

        query = f"""
                CREATE TABLE IF NOT EXISTS {table['name']}({', '.join(table['columns'])});
                """
        
        self.query(query)
        
    def insert(self, request):
        """
        
        """

        query = f"""
                INSERT INTO {request['table']}
                VALUES ("{request["state"]}", {request["action"]}, {request["reward"]})
                ;
                """
        
        self.query(query)


    def update(self, request):
        query = f"""
                UPDATE {request["table"]}
                SET reward = {request["reward"]}
                WHERE state = "{request["state"]}" AND action = {request["action"]};
                """
        
        self.query(query)

    def get_value(self, request):
        query = f"""
                SELECT * FROM {request["table"]}
                WHERE state = "{request["state"]}" AND action = {request["action"]};
                """
        
        res = self.query(query)
        return res.fetchall()

    def close(self):
        """
        Close database connection
        """

        self.connection.close()

    def delete(self):
        """
        Delete database file
        """
        os.remove(self.name)