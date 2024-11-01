from flask import Blueprint, render_template, request, redirect

from models.base import Session
from models.pizza import Pizza
from models.ingredient import Ingredient
from data.wheather import get_wheather


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")

    if 26 > wheather.get("temp") > 10:
        pizza_name = "Тепла"
    elif wheather.get("temp") <= 10:
        pizza_name = "Холодна"
    elif wheather.get("temp") > 26:
        pizza_name = "Пепероні"

    return render_template("index.html", title="Моя супер піцерія", wheather=wheather, pizza_name=pizza_name)


@pizza_route.get("/menu/")
def menu():
    wheather = get_wheather("Kyiv")
    with Session() as session:
        pizzas = session.query(Pizza).all()
        ingredients = session.query(Ingredient).all()

        context = {
            "pizzas": pizzas,
            "ingredients": ingredients,
            "title": "Мега меню",
            "wheather": wheather
        }
        return render_template("menu.html", **context)


@pizza_route.post("/add_pizza/")
def add_pizza():
    with Session() as session:
        name = request.form.get("name")
        price = request.form.get("price")

        ingredients = request.form.getlist("ingredients")
        ingredients = session.query(Ingredient).where(Ingredient.id.in_(ingredients)).all()

        pizza = Pizza(name=name, price=price, ingredients=ingredients)
        session.add(pizza)
        session.commit()
        return redirect("/menu/")
    

@pizza_route.route("/edit_pizza/<int:id>", methods=["GET", "POST"])
def edit_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).get(id)
        if request.method == "POST":
            pizza.name = request.form.get("name")
            pizza.price = float(request.form.get("price"))
            ingredients = request.form.getlist("ingredients")
            pizza.ingredients = session.query(Ingredient).filter(Ingredient.id.in_(ingredients)).all()
            session.commit()
            return redirect("/menu/")
        ingredients = session.query(Ingredient).all()
        return render_template("edit_pizza.html", pizza=pizza, ingredients=ingredients)


@pizza_route.route("/delete_pizza/<int:id>", methods=["POST"])
def delete_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).get(id)
        session.delete(pizza)
        session.commit()
    return redirect("/menu/")
