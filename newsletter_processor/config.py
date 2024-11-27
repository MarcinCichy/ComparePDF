import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Pobieranie danych z pliku .env
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL")

# Sprawdzanie, czy dane zostały załadowane
if not CLAUDE_API_KEY or not CLAUDE_API_URL:
    raise EnvironmentError("Brak wymaganych zmiennych środowiskowych: CLAUDE_API_KEY lub CLAUDE_API_URL.")
