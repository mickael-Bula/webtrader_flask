from flask import Flask, render_template

from database import get_stocks_from_db, get_db_engine

app = Flask(__name__)

# Initialise le moteur de base de données au démarrage de l'application
db_engine = get_db_engine()


@app.route('/')
def home():
    # Données statiques pour le test
    latest_stock = {
        'closing': 7850.50
    }

    user_data = {
        'lastHigher': 7950.25,
        'formattedDateOfLastHigher': '2025-05-15',
        'buyLimit': 7450.00,
        'runningPositions': [
            {
                'bought': '2025-06-20',
                'quantity': 100,
                'trade': 'CAC40',
                'lvcBuyTarget': 105.50,
                'buyTarget': 7800.00,
                'LvcSelleTarget': 110.00,
                'sellTarget': 8100.00
            }
        ],
        'waitingPositions': [
            {
                'validity': '2025-09-30',
                'quantity': 50,
                'trade': 'CAC40',
                'lvcBuyTarget': 95.00,
                'buyTarget': 7000.00,
                'LvcSelleTarget': 100.00,
                'sellTarget': 7400.00
            }
        ]
    }

    # Récupérer les données de la base de données
    stocks = get_stocks_from_db(engine=db_engine, table_name='cac_daily')

    # Calculs pour les valeurs dynamiques
    delta = ((latest_stock['closing'] - stocks[0]['open']) / stocks[0]['open']) * 100
    spread_to_execution = ((latest_stock['closing'] - user_data['buyLimit']) / user_data['buyLimit']) * 100

    return render_template(
        'index.html',
        latest_stock=latest_stock,
        user_data=user_data,
        stocks=stocks,
        delta=f'{delta:.2f}',
        spreadToExecution=f'{spread_to_execution:.2f}',
        flash_message=None,  # pour le moment, pas de message
        flash_type=None
    )


if __name__ == '__main__':
    app.run(debug=True)
