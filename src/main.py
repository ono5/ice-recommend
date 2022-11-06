from typing import Union
import logging

import settings
from forms.forms import RateForm, YesOrNoForm
from models.rate import Rate
from models.icecream import IceCream
from models.user import User

from flask import Flask, redirect, render_template, request, url_for

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER,
            static_folder=settings.STATIC_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "POST":
        user_name = request.form.get("user_name").strip()
        user = User.get_or_create(user_name)
        for icecream_name in request.form:
            if "user_name" != icecream_name:
                icecream = IceCream.get_or_create(icecream_name)
                rate_str = request.form.get(icecream_name).strip()
                value = int(rate_str)
                Rate.update_or_create(user, icecream, value)
        icecreams = Rate.recommend_icecream(user)
        return render_template("recommend_icecream.html", user_name=user_name, icecreams=icecreams)

    icecreams = IceCream.get_icecream_random()
    return render_template("index.html", icecreams=icecreams)


if __name__ == "__main__":
    app.run(debug=True, port=settings.PORT)
