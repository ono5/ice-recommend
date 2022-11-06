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
        icecreams = Rate.recommend_icecream(user)
        if icecreams:
            form = YesOrNoForm(request.form)
            form.user_name.data = user_name
            return render_template("recommend_icecream.html", user_name=user_name, icecreams=icecreams, form=form)

        form = RateForm(request.form)
        form.user_name.data = user_name
        return render_template("evaluate_icecream.html", user_name=user_name, form=form)

    return render_template("index.html")


@app.route("/icecream/evaluate/status", methods=["GET", "POST"])
def evaluate_yes_or_no() -> str:
    if request.method == "POST":
        form = YesOrNoForm(request.form)
        user_name = form.user_name.data.strip()
        if form.value.data == "No":
            return render_template("good_bye.html", user_name=user_name)

        form = RateForm(request.form)
        form.user_name.data = user_name
        return render_template("evaluate_icecream.html", user_name=user_name, form=form)
    return redirect(url_for("hello"))


@app.route("/icecream/rate", methods=["GET", "POST"])
def icecream_rate() -> Union[str, "Response"]:
    form = RateForm(request.form)
    if request.method == "POST":
        user_name = form.user_name.data.strip()
        user = User.get_or_create(user_name)
        icecream_name = form.icecream.data.strip()
        icecream = IceCream.get_or_create(icecream_name)
        value = int(form.rate.data)
        Rate.update_or_create(user, icecream, value)

        return render_template("good_bye.html", user_name=user_name)
    return redirect(url_for("hello"))

if __name__ == "__main__":
    app.run(debug=True, port=settings.PORT)
