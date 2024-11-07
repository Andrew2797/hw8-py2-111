from flask import Flask, render_template, request, redirect, url_for

from routes.pizza import pizza_route
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.base import create_db


app = Flask(__name__)


app.register_blueprint(pizza_route)
pizzas = [
    {"id": 1, "name": "Маргарита", "price": 150, "votes": 0},
    {"id": 2, "name": "Пепероні", "price": 180, "votes": 0}
]

@app.route("/")
def index():
    return render_template("index.html", pizzas=pizzas)


@app.route("/vote", methods=["POST"])
def vote():
    pizza_name = request.form.get("pizza_choice")
    for pizza in pizzas:
        if pizza["name"] == pizza_name:
            pizza["votes"] += 1
            break
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
