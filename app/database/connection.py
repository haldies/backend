from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            database="absensi_db"
        )
        print("Koneksi berhasil!")
        connection.close()
    except OperationalError as e:
        print(f"Error: {e}")


test_connection()

Base = declarative_base()

engine = create_engine("postgresql://postgres:postgres@localhost:5432/absensi_db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabel telah dibuat.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
