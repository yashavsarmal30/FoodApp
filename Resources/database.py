import os
from dotenv import load_dotenv
import psycopg2
from typing import Tuple, List, Any
 
load_dotenv()  # Load environment variables from .env file

class Database:
    _connection = None

    @classmethod
    def _get_connection(cls):
        if not cls._connection:
            database = os.getenv('Database')
            user = os.getenv('User_name')
            host = os.getenv('URL')
            password = os.getenv('DB_PASS')
            port = '5432'  # Default Port Number For PostgreSQL

            try:
                cls._connection = psycopg2.connect(
                    dbname=database, user=user,
                    password=password, host=host, port=port
                )
            except Exception as e:
                print(f"Error connecting to database: {e}\nCheck Your .env Fle Credentials")
        return cls._connection

    @classmethod
    def execute(cls, query: str, params: Tuple = None, fetch: bool = False) -> List[Tuple[Any]]:
        """
        Executes a SQL query on the database.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters to be passed to the query (for parameterized queries). Defaults to None.
            fetch (bool, optional): Whether to fetch results after execution. Defaults to False.

        Returns:
            list or None: If fetch is True, returns a list of results. Otherwise, None.
        """
        try:
            connection = cls._get_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
        return []

    @classmethod
    def close(cls):
        """
        Closes the connection to the database.
        """
        if cls._connection:
            cls._connection.close()
            cls._connection = None
    

if __name__ == '__main__':
    print("Run >>>>>>>>  main.py <<<<<<<< File")
