import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username is already in use, please try another")
            return redirect(url_for("register"))
        # confirm password
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-pass")
        if password != confirm_password:
            flash("The password doesn't match")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("You Have Successfully Registered")
        return redirect(url_for("my_recipes", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "my_recipes", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("my_recipes.html", username=username)
    
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_time": request.form.get("recipe_time"),
            "recipe_tools": request.form.getlist("recipe_tools"),
            "recipe_instructions": request.form.get("recipe_instructions"),
            "recipe_ingredients": request.form.getlist("recipe_ingredients"),
            "recipe_type": request.form.get("recipe_type"),
            "created_by": session["user"],
            "allergens": request.form.get("allergens")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("You're recipe has been added")
        return redirect(url_for("get_recipes"))
    cuisine = mongo.db.cuisine.find().sort("cuisine_type", 1)
    return render_template("add_recipe.html", cuisine=cuisine)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        submit = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_time": request.form.get("recipe_time"),
            "recipe_tools": request.form.getlist("recipe_tools"),
            "recipe_instructions": request.form.get("recipe_instructions"),
            "recipe_ingredients": request.form.getlist("recipe_ingredients"),
            "recipe_type": request.form.get("recipe_type"),
            "created_by": session["user"],
            "allergens": request.form.get("allergens")
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)},submit)
        flash("You're recipe has been successfully Edited!")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisine = mongo.db.cuisine.find().sort("cuisine_type", 1)
    return render_template("edit_recipe.html", recipe=recipe, cuisine=cuisine)


@app.route("/delete_recipe, <recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("You have successfully delteted your recipe")
    return redirect(url_for("get_recipes"))


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
