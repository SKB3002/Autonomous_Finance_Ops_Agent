import json
import psycopg2
from datetime import datetime


def log_event(run_id, agent_name, action, input_data, output_data):
    """
    Writes an immutable audit log entry.
    """

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
        INSERT INTO audit_logs (run_id, agent_name, action, input_data, output_data, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            run_id,
            agent_name,
            action,
            json.dumps(input_data),
            json.dumps(output_data),
            datetime.utcnow()
        )
    )

    conn.commit()
    cur.close()
    conn.close()

