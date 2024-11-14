import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))
from flask import Flask, render_template
from api.etherscan import get_transactions

app = Flask(__name__)

@app.route('/')
def home():
    address = '0x8bC43A1810a178FB28e91bCa06D437C74df33250'  # Замените на адрес Ethereum-кошелька
    transactions = get_transactions(address)
    return render_template('index.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
