import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Charge les variables d'environnement
dotenv_file = ".env.local"
load_dotenv(dotenv_path=dotenv_file)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_db_engine() -> Engine:
    """Crée et retourne l'objet moteur de la base de données."""
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError(
            f"Erreur : Les variables de connexion à la base de données "
            + "ne sont pas définies dans le fichier {dotenv_file}.")

    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def get_stocks_from_db(engine: Engine, table_name: str) -> list[dict]:
    """Récupère les cotations en base de données."""
    with engine.connect() as conn:
        # Correction de la requête SQL pour sélectionner les colonnes individuellement
        query = text(
            f'SELECT "date", "high", "low", "open", "close" '
            f'FROM "{table_name}" '
            f'ORDER BY "date" DESC '
            f'LIMIT 10'
        )

        # Utilisation de fetchall() pour récupérer toutes les lignes
        result = conn.execute(query).fetchall()

        # Conversion des données brutes en une liste de dictionnaires
        stocks = []
        for row in result:
            stocks.append({
                'date': row.date.strftime('%Y-%m-%d'),  # Formatage de la date en chaîne de caractères
                'open': float(row.open),
                'high': float(row.high),
                'low': float(row.low),
                'close': float(row.close)
            })

        return stocks
