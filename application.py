import os
from flask import Flask, redirect, url_for, request, render_template
from forms import RecipeForm
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IKUVGGuiyfvYVIvkJBOLUIBOUB89IOUBV98b'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')

@app.route('/')
def hello_world():
    """
    Function to show example instance
    :return:
    """
    return render_template('index.html')

# @app.route('/add_recipe', methods = ['POST', 'GET'])
# def add_recipe():
#     """
#     Function add a recipe using a manual form
#     :return:
#     """
#     if request.method == 'POST':
#         add_recipe = request.form['name']
#         print(add_recipe)
#         return "Recipe added successfully"
#     else:
#         return render_template('add_recipe.html')

@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        ingredients_names = form.ingredients_names.data
        preparation_inst = form.preparation_inst.data
        dish_picture = form.dish_picture.data
        pic_filename = dish_picture.lower().replace(" ", "_") + '.' + secure_filename(form.dish_picture.data.filename).split('.')[-1]
        form.dish_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'], pic_filename))
        recipes_file = os.path.join(app.root_path, 'recipes.csv')
        df = pd.DataFrame([{'name': recipe_name, 'ing': ingredients_names, 'prep': preparation_inst, 'pic': pic_filename}])
        if os.path.exists(recipes_file):
            df.to_csv(recipes_file, mode='a', header=False, index=False)
        else:
            df.to_csv(recipes_file, index=False)
        return redirect(url_for('hello_world'))
    else:
        return render_template('add_recipe.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = []
        for file in os.listdir(app.config['SUBMITTED_DATA']):
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'], file))
                if query.lower() in df['name'].iloc[0].lower() or \
                   query.lower() in df['ing'].iloc[0].lower() or \
                   query.lower() in df['prep'].iloc[0].lower():
                    results.append(df)
        return render_template('search_results.html', results=results)
    else:
        return render_template('search.html')

@app.route('/remove_recipe', methods=['GET', 'POST'])
def remove_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        recipe_file = os.path.join(app.config['SUBMITTED_DATA'], recipe_name.lower().replace(" ", "_") + '.csv')
        if os.path.exists(recipe_file):
            df = pd.read_csv(recipe_file)
            pic_filename = df['pic'].iloc[0]
            os.remove(recipe_file)
            os.remove(os.path.join(app.config['SUBMITTED_IMG'], pic_filename))
            return "Recipe removed successfully"
        else:
            return "Recipe not found"
    else:
        return render_template('remove_recipe.html')


@app.route('/view_recipe/<recipe_name>')
def view_recipe(recipe_name):
    recipes_file = os.path.join(app.root_path, 'recipes.csv')
    if os.path.exists(recipes_file):
        df = pd.read_csv(recipes_file)
        selected_recipe = df[df['name'].str.lower() == recipe_name.lower()]
        if not selected_recipe.empty:
            recipe = selected_recipe.iloc[0]
        else:
            recipe = {'name': 'Default Recipe', 'ing': 'Default Ingredients', 'prep': 'Default Instructions',
                      'pic': 'default.jpg'}
    else:
        recipe = {'name': 'Default Recipe', 'ing': 'Default Ingredients', 'prep': 'Default Instructions',
                  'pic': 'default.jpg'}

    return render_template('view_recipe.html', recipe=recipe)

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