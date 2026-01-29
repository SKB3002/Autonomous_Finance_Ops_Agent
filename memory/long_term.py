import psycopg2


def write_persistent_memory(key, value, source="user_approved"):
    conn = psycopg2.connect(
        dbname="financeops",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO persistent_memory (key, value, source)
        VALUES (%s, %s, %s)
        ON CONFLICT (key) DO UPDATE
        SET value = EXCLUDED.value,
            source = EXCLUDED.source
        """,
        (key, value, source)
    )

    conn.commit()
    cur.close()
    conn.close()

