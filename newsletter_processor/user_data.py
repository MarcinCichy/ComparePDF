from typing import Dict, Any


def get_user_data(user_email: str, conn) -> Dict[str, Any]:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, user_email, user_prefs, desired_word_limit
            FROM users
            WHERE user_email = %s;
        """, (user_email,))
        user_data = cursor.fetchone()
    return {
        "id": user_data[0],
        "user_email": user_data[1],
        "user_prefs": user_data[2],
        "desired_word_limit": user_data[3]
    } if user_data else None
