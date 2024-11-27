from db_manager import connect_to_db, insert_email, get_pending_emails, update_email_record
from email_handler import fetch_emails_from_disk
from user_data import get_user_data
from summary_generator import generate_summary


def main():
    conn = connect_to_db()
    if not conn:
        return

    try:
        print("Pobieranie i czyszczenie emaili...")
        emails = fetch_emails_from_disk()
        for email_data in emails:
            email_id = insert_email(email_data, conn)
            print(f"Zapisano email z ID: {email_id}")

        print("Przetwarzanie oczekujących wiadomości...")
        pending_emails = get_pending_emails(conn)
        for email in pending_emails:
            user_data = get_user_data(email["user_email"], conn)
            if user_data:
                summaries = generate_summary(
                    content=email["email_content"],
                    user_prefs=user_data["user_prefs"],
                    word_limit=user_data["desired_word_limit"]
                )
                update_email_record(email["id"], summaries, conn)
                print(f"Przetworzono email z ID: {email['id']}")
            else:
                print(f"Nie znaleziono danych użytkownika dla emaila: {email['user_email']}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        conn.close()
        print("Zakończono proces.")


if __name__ == "__main__":
    main()
