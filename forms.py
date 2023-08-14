from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    recipe_name = StringField('Name of Dish:', validators=[DataRequired()])
    ingredients_names = TextAreaField('Ingredients:', validators=[DataRequired()])
    preparation_inst = TextAreaField('Preparation Instructions:', validators=[DataRequired()])
    dish_picture = FileField('Picture of cooked dish:', validators=[FileRequired()])

