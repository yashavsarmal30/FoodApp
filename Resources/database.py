import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse
from typing import Tuple, List, Any

load_dotenv()  # Load environment variables from .env file

class Database:
    _connection = None

    @classmethod
    def _get_connection(cls):
        if not cls._connection:
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                print("❌ DATABASE_URL not found in .env file.")
                return None

            try:
                result = urlparse(db_url)

                cls._connection = psycopg2.connect(
                    dbname=result.path[1:],   # Remove the leading '/'
                    user=result.username,
                    password=result.password,
                    host=result.hostname,
                    port=result.port,
                    sslmode='require'
                )
                print("✅ Connected to NeonDB successfully.")
            except Exception as e:
                print(f"❌ Error connecting to NeonDB: {e}\nCheck your .env file credentials.")
        return cls._connection

    @classmethod
    def execute(cls, query: str, params: Tuple = None, fetch: bool = False) -> List[Tuple[Any]]:
        try:
            connection = cls._get_connection()
            if not connection:
                return []

            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error executing query: {e}")
        return []

    @classmethod
    def close(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            print("🔒 Connection to NeonDB closed.")

if __name__ == '__main__':
    print("▶️ Run >>>>>>>>  main.py <<<<<<<< File")
