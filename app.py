from flask import Flask, render_template

app = Flask(__name__)


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

    stocks = [
        {'date': '2025-07-25', 'opening': 7800.00, 'higher': 7880.50, 'lower': 7750.25, 'closing': 7850.50},
        {'date': '2025-07-24', 'opening': 7750.25, 'higher': 7820.10, 'lower': 7700.50, 'closing': 7780.45},
        {'date': '2025-07-23', 'opening': 7650.15, 'higher': 7780.20, 'lower': 7640.80, 'closing': 7750.25},
        {'date': '2025-07-22', 'opening': 7700.50, 'higher': 7720.90, 'lower': 7600.10, 'closing': 7650.15},
    ]

    # Calculs pour les valeurs dynamiques
    delta = ((latest_stock['closing'] - stocks[0]['opening']) / stocks[0]['opening']) * 100
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
