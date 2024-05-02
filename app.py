import os
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime, timedelta

from datetime import date
from flask import jsonify
from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests


# Define a flask app
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['UPLOAD_FOLDER'] ="./static/predictimgs"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


#star new code start

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)  # Ensure it's defined as a Date type

    def __repr__(self):
        return f"Inventory(id={self.id}, user_id={self.user_id}, item_name={self.item_name}, expiry_date={self.expiry_date})"

# Model saved with Keras model.save()
#MODEL_PATH = os.path.join("models","keras_models", "model-mobilenet-RMSprop0.0002-001-0.930507-0.647776.h5")
MODEL_PATH = os.path.join("models","keras_models", "model-mobilenet-RMSprop0.0002-008-0.995584-0.711503.h5")
                                              
# Load your trained model
model = load_model(MODEL_PATH)
print("Model loaded successfully !! Check http://127.0.0.1:5000/")

with open(os.path.join("static","food_list", "food_list.json"), "r", encoding="utf8") as f:
    food_labels = json.load(f)
class_names = sorted(food_labels.keys())
label_dict = dict(zip(range(len(class_names)), class_names))

food_calories = pd.read_csv(os.path.join("static","food_list", "Food_calories.csv"))

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    # Preprocessing the image
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    return x

#caution code start
FOOD_RECIPES_FILE_PATH = "static/food_list/Food_recipes_kitchensync.csv" 

def get_recipe_recommendations(expiring_items):
    # Read the Excel file into a DataFrame
    recipes_df = pd.read_csv(FOOD_RECIPES_FILE_PATH)

    # Initialize an empty list to store recommended recipes
    recommended_recipes = []

    # Iterate over each expiring item
    for item in expiring_items:
        # Get recipes that contain the expiring item as an ingredient
        matching_recipes = recipes_df[recipes_df['Ingredients'].str.contains(item)]

        # If there are matching recipes, add them to the recommended recipes list
        if not matching_recipes.empty:
            for _, recipe in matching_recipes.iterrows():
                # Check if the recipe is already in the recommended recipes list
                if recipe.Title not in [rec['title'] for rec in recommended_recipes]:
                    # Append the title, ingredients, and instructions to the recommended recipes list
                    recommended_recipes.append({
                        'title': recipe.Title,
                        'ingredients': recipe.Ingredients,
                        'instructions': recipe.Instructions
                    })

    # Return the list of recommended recipes, limited to 5 recipes
    return recommended_recipes[:5]



def get_expiring_items(items):
    print("Items:", items)  # Add this line for debugging

    # Get the current date
    current_date = datetime.now().date()

    # Calculate the number of days until expiry for each item
    for item in items:
        item.days_until_expiry = (item.expiry_date - current_date).days

    # Sort the items by days until expiry in ascending order
    sorted_items = sorted(items, key=lambda x: x.days_until_expiry)

    # Get the top 3 expiring items
    expiring_items = sorted_items[:3]

    # Extract the names of the expiring items
    expiring_item_names = [item.item_name for item in expiring_items]

    return expiring_item_names

#caution code end


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# star code new start

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        item_name = request.form['item_name']
        expiry_date = request.form['expiry_date']
        new_item = Inventory(user_id=current_user.id, item_name=item_name, expiry_date=expiry_date)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        # items = Inventory.query.filter_by(user_id=current_user.id).all()
        # expiring_items = []
        # for item in items:
        #     days_until_expiry = (item.expiry_date - datetime.now().date()).days
        #     expiring_items.append((item.item_name, days_until_expiry))
        # # Sort expiring_items based on days_until_expiry
        # expiring_items.sort(key=lambda x: x[1])
        # # Take the top 3 items
        # expiring_items = expiring_items[:3]

        # Get items from inventory
        items = Inventory.query.filter_by(user_id=current_user.id).all()

        # Get top 3 expiring items
        expiring_items = get_expiring_items(items)

        # Get recommended recipes based on expiring items
        recommended_recipes = get_recipe_recommendations(expiring_items)

        return render_template('dashboard.html', items=items, expiring_items=expiring_items, recommended_recipes=recommended_recipes)

        # return render_template('dashboard.html', items=items, expiring_items=expiring_items)


# New route and function to fetch expiring items information
@app.route('/fetch_expiring_items_info', methods=['POST'])
def fetch_expiring_items_info():
    # Get expiring items from the request
    expiring_items = request.json.get('expiring_items', [])

    # Initialize an empty list to store expiring items information
    expiring_items_info = []

    # Get the current date
    current_date = datetime.now().date()

    # Calculate the number of days until expiry for each item
    for item in expiring_items:
        # Convert item to string
        item_str = str(item)

        # Get the expiry date from the database
        expiry_date = Inventory.query.filter_by(item_name=item_str).first().expiry_date

        # Calculate the days until expiry
        days_until_expiry = (expiry_date - current_date).days

        # Append the item and days_until_expiry to the expiring items info list
        expiring_items_info.append({
            'item': item_str,
            'days_until_expiry': days_until_expiry
        })

    # Return the list of expiring items information
    return jsonify(expiring_items_info)



@app.route('/add_task', methods=['POST'])
def add_task():
    item_name = request.form['item_name']
    expiry_date_str = request.form['expiry_date']
    
    # Print out the expiry_date_str to see its format
    print("Expiry Date String:", expiry_date_str)

    # Convert the expiry_date string to a Python date object
    expiry_date = date.fromisoformat(expiry_date_str)

    # Insert the item into the inventory table
    new_item = Inventory(user_id=current_user.id, item_name=item_name, expiry_date=expiry_date)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'})





@app.route('/delete_item', methods=['POST'])
def delete_item():
    # Get the item ID from the JSON request
    item_id = int(request.json['item_id'])
    
    # Query the database to find the item by its ID
    item_to_delete = Inventory.query.get(item_id)
    
    if item_to_delete:
        # If the item exists, delete it from the database
        db.session.delete(item_to_delete)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        # If the item does not exist, return an error message
        return jsonify({'error': 'Item not found'}), 404



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/get_recipes')
def get_recipes():
    # Get top 3 expiring items
    items = Inventory.query.filter_by(user_id=current_user.id).all()
    expiring_items = get_expiring_items(items)
    
    # Get recommended recipes based on expiring items
    recommended_recipes = get_recipe_recommendations(expiring_items)

    return jsonify(recommended_recipes)


@app.route("/predictthedish", methods=["GET"])
def predictthedish():
    return render_template('Know_Before_You_Eat.html')  


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = {}
        # Get the file from the POST request
        file = request.files["image"]

        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Make prediction
        image = prepare_image(filepath)
        preds = model.predict(image)
        predictions = preds.argmax(axis=-1)[0]
        pred_label = label_dict[predictions]

        # Fetch additional nutritional information from Spoonacular API
        spoonacular_api_key = "227a4d1c643048d785e6c5401e3f3d81"
        spoonacular_url = f"https://api.spoonacular.com/recipes/guessNutrition?apiKey={spoonacular_api_key}&title={pred_label}"
        response = requests.get(spoonacular_url)
        if response.status_code == 200:
            spoonacular_data = response.json()
            print("Spoonacular API Response:", spoonacular_data)  # Debugging print statement

            # Debugging print statements for nutritional information
            if 'calories' in spoonacular_data:
                data['calories'] = spoonacular_data['calories']['value']
                print("Calories:", data['calories'])  # Debugging print statement
            else:
                print("Warning: 'calories' key not found in Spoonacular API response")  # Debugging print statement

            if 'fat' in spoonacular_data:
                data['fat'] = spoonacular_data['fat']['value']
                print("Fat:", data['fat'])  # Debugging print statement
            else:
                print("Warning: 'fat' key not found in Spoonacular API response")  # Debugging print statement

            if 'protein' in spoonacular_data:
                data['protein'] = spoonacular_data['protein']['value']
                print("Protein:", data['protein'])  # Debugging print statement
            else:
                print("Warning: 'protein' key not found in Spoonacular API response")  # Debugging print statement

            if 'carbs' in spoonacular_data:
                data['carbs'] = spoonacular_data['carbs']['value']
                print("Carbs:", data['carbs'])  # Debugging print statement
            else:
                print("Warning: 'carbs' key not found in Spoonacular API response")  # Debugging print statement

            # Construct response data
            data = {
                "pred_label": pred_label,
                "calories": data.get("calories"),
                "fat": data.get("fat"),
                "protein": data.get("protein"),
                "carbs": data.get("carbs")
            }

            return jsonify(data)
        else:
            print("Error: Failed to fetch data from Spoonacular API. Status Code:", response.status_code)  # Debugging print statement
            return jsonify({"error": "Failed to fetch data from Spoonacular API."}), 500

    return jsonify({"error": "Method not allowed."}), 405

if __name__ == "__main__":
    # Serve the app with gevent
    app.run(debug=True)
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()