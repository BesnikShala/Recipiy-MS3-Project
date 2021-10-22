import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to log in first!")
            return redirect(url_for("login"))
    return wrap

# get recipes list form db
@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/get_user_recipes")
def get_user_recipes():
    user_recipe = list(mongo.db.recipes.find())
    return render_template("my_recipes.html", user_recipe=user_recipe)


# search recipes
@app.route("/search", methods=["GET", "POST"])
def search():
    searcher = request.form.get("searcher")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": searcher}}))
    return render_template("recipes.html", recipes=recipes)

# register account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # check if username already exists
        if existing_user:
            flash("This username is already in use, please try another")
            return redirect(url_for("register"))
        # confirm password
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-pass")
        if password != confirm_password:
            flash("The password doesn't match")
            return redirect(url_for("register"))

        user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "user_recipes": []
        }
        mongo.db.users.insert_one(user)

        session["user"] = request.form.get("username").lower()
        flash("You Have Successfully Registered")
        return redirect(url_for("my_recipes", username=session["user"]))

    return render_template("register.html")

# login to account
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # check user detail and redirect to profile
        if existing_user:
            # make sure hashed password matches entered password
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
            # if user details are incorrect flash message
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# log user out by ending session
@app.route("/logout")
@login_required
def logout():
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("login"))

# add recipe
@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    if request.method == "POST":
        recipe = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_time": request.form.get("recipe_time"),
            "recipe_tools": request.form.getlist("recipe_tools"),
            "recipe_instructions": request.form.getlist("recipe_instructions"),
            "recipe_ingredients": request.form.getlist("recipe_ingredients"),
            "recipe_type": request.form.get("recipe_type"),
            "created_by": session["user"],
            "allergens": request.form.get("allergens"),
            "image_url": request.form.get("image_url")
        }

        newID = mongo.db.recipes.insert_one(recipe)

        mongo.db.users.update_one(
            {"username": session["user"]},
            {"$push": {"user_recipes": newID.inserted_id}})
        flash("You have successfully added your recipe")

        return redirect(url_for("view_recipe", recipe_id=newID.inserted_id))
    cuisine = mongo.db.cuisine.find().sort("cuisine_type", 1)
    instruction = mongo.db.recipes.find().sort("recipe_instructions", 1)
    categories = mongo.db.categories.find().sort("recipe_type", 1)
    return render_template(
        "add_recipe.html", cuisine=cuisine, instruction=instruction, categories=categories)

# edit recipe details
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    if request.method == "POST":
        submit = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_time": request.form.get("recipe_time"),
            "recipe_tools": request.form.getlist("recipe_tools"),
            "recipe_instructions": request.form.getlist("recipe_instructions"),
            "recipe_ingredients": request.form.getlist("recipe_ingredients"),
            "recipe_type": request.form.get("recipe_type"),
            "created_by": session["user"],
            "allergens": request.form.get("allergens"),
            "image_url": request.form.get("image_url")
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("You're recipe has been successfully Edited!")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisine = mongo.db.cuisine.find().sort("cuisine_type", 1)
    instruction = mongo.db.recipes.find().sort("recipe_instructions", 1)
    utensils = mongo.db.recipes.find().sort("recipe_tools", 1)
    categories = mongo.db.categories.find().sort("recipe_type", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe,
        cuisine=cuisine,
        categories=categories,
        utensils=utensils,
        instruction=instruction)


# show user profile when logged in
@app.route("/my_recipes/<username>", methods=["GET", "POST"])
@login_required
def my_recipes(username):
    # get session user details from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    favourites = list(mongo.db.favourites.find(
        {"username": session["user"]}))

    if session["user"]:
        return render_template(
            "my_recipes.html", username=username, favourites=favourites)

    return redirect(url_for("login"))


@app.route("/add_favourites/<recipe_id>", methods=["GET", "POST"])
def add_favourites(recipe_id):

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    print(username)
    print(request)

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    print(recipe)
    recipe_name = "".join(recipe["recipe_name"]),
    recipe_description = "".join(recipe["recipe_description"]),
    image_url = recipe["image_url"]
    
    info = {
        "recipe_id": recipe_id,
        "recipe_name": recipe_name,
        "recipe_description": recipe_description,
        "username": username,
        "image_url": image_url
    }
    mongo.db.favourites.insert_one(info)
    flash("Recipe saved to favourites")

    return redirect(url_for(
        "my_recipes", username=username, recipe_id=recipe_id))

# delete recipe
@app.route("/delete_recipe/, <recipe_id>")
@login_required
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("You have successfully delteted your recipe")
    return redirect(url_for("get_recipes"))


# view recipe details
@app.route("/view_recipe/<recipe_id>") 
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    print(recipe)
    return render_template("view_recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
