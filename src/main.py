import logging

import settings

from flask import Flask, render_template

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)

app = Flask(__name__, static_folder='./static/images')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
