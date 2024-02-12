import psycopg
import os

env = os.environ
host = env['PG_HOST']
db = env['PG_DB']
user = env['PG_USER']
pw = env['PG_PASS']

def set(table, key, value):
    try:
        with psycopg.connect(f"dbname={db} user={user} password={pw} host={host} sslmode='require'") as conn:
            with conn.cursor() as cur:
                # Create table if it doesn't exist
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS {table} (
                        id SERIAL PRIMARY KEY,
                        key TEXT NOT NULL UNIQUE,
                        value TEXT NOT NULL
                    );
                    """.format(table=table)
                )

                # Insert or update the record
                cur.execute(
                    """
                    INSERT INTO {table} (key, value)
                    VALUES (%s, %s)
                    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
                    """.format(table=table),
                    (key, value)
                )
    except (Exception, psycopg.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def get(table, key):
    try:
        with psycopg.connect(f"dbname={db} user={user} password={pw} host={host} sslmode='require'") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT value FROM {table} WHERE key = '{key}'")
                result = cur.fetchone()
                return result[0] if result else None
    except (Exception, psycopg.Error) as error:
        print("psycopg: ", error)
        return None
