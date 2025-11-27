from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User, PantryItem, Recipe, SavedRecipe
from ai_engine import RecipeRecommender, create_sample_recipes
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# AI Engine
recommender = RecipeRecommender()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return "Username already exists"
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Add pantry item
        ingredient_name = request.form['ingredient_name']
        quantity = request.form.get('quantity', '')
        category = request.form.get('category', 'Other')
        
        new_item = PantryItem(
            user_id=current_user.id,
            ingredient_name=ingredient_name,
            quantity=quantity,
            category=category
        )
        db.session.add(new_item)
        db.session.commit()
    
    pantry_items = PantryItem.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', pantry_items=pantry_items)

@app.route('/delete_pantry_item/<int:item_id>')
@login_required
def delete_pantry_item(item_id):
    item = PantryItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route('/find_recipes')
@login_required
def find_recipes():
    # Get user's pantry items
    pantry_items = PantryItem.query.filter_by(user_id=current_user.id).all()
    
    # Get all recipes
    all_recipes = Recipe.query.all()
    
    # Train recommender if not already trained
    if not recommender.recipe_vectors:
        recommender.fit(all_recipes)
    
    # Get recommendations
    recommendations = recommender.recommend_recipes(pantry_items)
    
    return render_template('recipes.html', recommendations=recommendinations)

@app.route('/recipe/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/save_recipe/<int:recipe_id>')
@login_required
def save_recipe(recipe_id):
    saved_recipe = SavedRecipe.query.filter_by(
        user_id=current_user.id, 
        recipe_id=recipe_id
    ).first()
    
    if not saved_recipe:
        new_saved = SavedRecipe(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new_saved)
        db.session.commit()
    
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Add sample recipes if none exist
        if Recipe.query.count() == 0:
            sample_recipes = create_sample_recipes()
            for recipe_data in sample_recipes:
                recipe = Recipe(**recipe_data)
                db.session.add(recipe)
            db.session.commit()

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
