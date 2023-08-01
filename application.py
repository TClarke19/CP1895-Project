from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = ""

# Define the path to the CSV file
csv_file_path = "recipes.csv"

# Load existing recipes from the CSV file into a DataFrame using Pandas
if os.path.exists(csv_file_path):
    recipes_df = pd.read_csv(csv_file_path)
else:
    recipes_df = pd.DataFrame(columns=["Image", "Ingredients", "Preparation", "Serving"])

# Function to validate image file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipes")
def display_recipes():
    return render_template("recipes.html", recipes=recipes_df.to_dict(orient="records"))

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        image_file = request.files["image"]
        ingredients = request.form["ingredients"]
        preparation = request.form["preparation"]
        serving = request.form["serving"]

        if not image_file or not allowed_file(image_file.filename):
            flash("Please upload a valid image file (png, jpg, jpeg, or gif).", "error")
            return redirect(url_for("add_recipe"))

        # Append the new recipe to the DataFrame
        new_recipe = {
            "Image": image_file.filename,
            "Ingredients": ingredients,
            "Preparation": preparation,
            "Serving": serving,
        }
        recipes_df.loc[len(recipes_df)] = new_recipe
        recipes_df.to_csv(csv_file_path, index=False)

        flash("Recipe added successfully!", "success")
        return redirect(url_for("display_recipes"))

    return render_template("add_recipe.html")

@app.route("/remove_recipe/<int:recipe_id>")
def remove_recipe(recipe_id):
    # Remove the recipe from the DataFrame based on its index
    recipes_df.drop(index=recipe_id, inplace=True)
    recipes_df.to_csv(csv_file_path, index=False)
    flash("Recipe removed successfully!", "success")
    return redirect(url_for("display_recipes"))

if __name__ == "__main__":
    app.run(debug=True)