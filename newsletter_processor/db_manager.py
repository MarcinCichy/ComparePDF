import psycopg2
from psycopg2 import sql
from typing import List, Dict, Any

DB_CONFIG = {
    'dbname': 'nazwa_bazy',
    'user': 'uzytkownik',
    'password': 'haslo',
    'host': 'adres_hosta',
    'port': 'port'
}


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Połączono z bazą danych.")
        return conn
    except Exception as e:
        print("Błąd połączenia z bazą danych:", e)


def insert_email(email_data: Dict[str, Any], conn) -> int:
    with conn.cursor() as cursor:
        insert_query = sql.SQL("""
            INSERT INTO emails (date, sender_email, content, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """)
        cursor.execute(insert_query, (
            email_data['date'],
            email_data['sender_email'],
            email_data['content'],
            'PENDING'
        ))
        email_id = cursor.fetchone()[0]
        conn.commit()
        return email_id


def get_pending_emails(conn) -> List[Dict[str, Any]]:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, user_email, email_content, status
            FROM emails
            WHERE status = 'PENDING';
        """)
        pending_emails = cursor.fetchall()
    return [{"id": row[0], "user_email": row[1], "email_content": row[2]} for row in pending_emails]


def update_email_record(email_id: int, summaries: Dict[str, str], conn) -> None:
    with conn.cursor() as cursor:
        update_query = """
            UPDATE emails
            SET general_summary = %s, personalized_summary = %s, status = 'PROCESSED'
            WHERE id = %s;
        """
        cursor.execute(update_query, (summaries["general_summary"], summaries["personalized_summary"], email_id))
        conn.commit()
