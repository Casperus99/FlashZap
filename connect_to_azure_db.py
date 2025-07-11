import psycopg2

# Zastąp tymi wartościami swoje dane połączeniowe
host = "flash-zap-db.postgres.database.azure.com"
dbname = "postgres"
user = "kanowa"
password = "Post-Casp99"
sslmode = "require"

# Utwórz parametry połączenia
conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"

try:
 # Połącz się z bazą danych
 conn = psycopg2.connect(conn_string)
 print("Pomyślnie połączono z bazą danych!")

 # Utwórz kursor do wykonywania operacji na bazie danych
 cursor = conn.cursor()

 # Przykład: Wykonaj zapytanie SQL
 cursor.execute("SELECT version();")
 record = cursor.fetchone()
 print("Wersja bazy danych PostgreSQL: ", record)

except Exception as e:
 print(f"Błąd połączenia z bazą danych: {e}")

finally:
 # Zamknij połączenie
 if 'conn' in locals() and conn is not None:
  cursor.close()
  conn.close()
  print("Połączenie z bazą danych zostało zamknięte.")