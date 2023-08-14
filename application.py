import os
from flask import Flask, redirect, url_for, request, render_template
from forms import RecipeForm
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir','')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir','')

@app.route('/')
def hello_world():
    """
    Function to show example instance
    :return:
    """
    return render_template('index.html')

@app.route('/add_recipe', methods = ['POST', 'GET'])
def add_recipe():
    """
    Function add a recipe using a manual form
    :return:
    """
    if request.method == 'POST':
        add_recipe = request.form['name']
        print(add_recipe)
        return "Recipe added successfully"
    else:
        return render_template('add_recipe.html')

@app.route('/add_beneficiary_auto', methods = ['POST', 'GET'])
def add_beneficiary_auto():
    """
    Function to use inbuilt methods to add a recipe, with file handling
    :return:
    """
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        ingredients_names = form.ingredients_names.data
        preparation_inst = form.preparation_inst.data
        dish_picture = form.dish_picture.data
        pic_filename = dish_picture.lower().replace(" ", "_") + '.' + secure_filename(form.dish_picture.data.filename).split('.')[-1]
        form.dish_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ing': ingredients_names, 'prep': preparation_inst, 'pic': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return redirect(url_for('hello_world'))
    else:
        return render_template('add_recipe.html', form=form)

@app.route('/admin')
def hello_admin():
    """
    Example for a sample page
    :return: string
    """
    return "Hello Admin"

@app.route('/guest/<guest>')
def hello_guest(guest):
    """
    Example for a sample page with variable
    :param guest: variable
    :return: String
    """
    return "Hello % as Guest" % guest

@app.route('/user/<user>')
def hello_user(user):
    """
    Function that demonstrates the usage of url for function
    :param user:
    :return:
    """
    if user=='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=user))

@app.route('/input', methods = ['POST', 'GET'])
def information():
    """
    Function that demonstrates an example of gathering form info
    :return:
    """
    if request.method == 'POST':
        info = request.form['info']
        return redirect(url_for('hello_guest', guest=info))
    else:
        return redirect(url_for('hello_world'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Standard error handling mechanism
    :param e: Error details
    :return:
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)