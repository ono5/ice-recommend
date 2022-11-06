import logging

import settings
from models.rate import Rate
from models.icecream import IceCream
from models.user import User

from flask import Flask, render_template

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER,
            static_folder=settings.STATIC_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=settings.PORT)
