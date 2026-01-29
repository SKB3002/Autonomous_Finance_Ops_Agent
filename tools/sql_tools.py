import psycopg2


def read_from_db(query: str):
    conn = psycopg2.connect(
        dbname="financeops",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def propose_db_write(statement: str):
    return {
        "statement": statement,
        "status": "proposed_only"
    }
