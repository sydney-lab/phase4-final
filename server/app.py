from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Models
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    recipes = db.relationship('Recipe', backref='user', cascade='all, delete-orphan')
    
    serialize_rules = ('-recipes.user',)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe', cascade='all, delete-orphan')
    ingredients = association_proxy('recipe_ingredients', 'ingredient')
    
    serialize_rules = ('-user.recipes', '-recipe_ingredients.recipe')

class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    recipe_ingredients = db.relationship('RecipeIngredient', backref='ingredient', cascade='all, delete-orphan')
    recipes = association_proxy('recipe_ingredients', 'recipe')
    
    serialize_rules = ('-recipe_ingredients.ingredient',)

class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    
    serialize_rules = ('-recipe.recipe_ingredients', '-ingredient.recipe_ingredients')

# Routes
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            user = User(name=data['name'], email=data['email'])
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        return jsonify([recipe.to_dict() for recipe in recipes]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            recipe = Recipe(
                title=data['title'],
                instructions=data['instructions'],
                cook_time=data['cook_time'],
                user_id=data['user_id']
            )
            db.session.add(recipe)
            db.session.commit()
            return jsonify(recipe.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/recipes/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def recipe_by_id(id):
    recipe = Recipe.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(recipe.to_dict()), 200
    
    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(recipe, key, value)
            db.session.commit()
            return jsonify(recipe.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    elif request.method == 'DELETE':
        db.session.delete(recipe)
        db.session.commit()
        return '', 204

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    if request.method == 'GET':
        ingredients = Ingredient.query.all()
        return jsonify([ingredient.to_dict() for ingredient in ingredients]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            ingredient = Ingredient(name=data['name'])
            db.session.add(ingredient)
            db.session.commit()
            return jsonify(ingredient.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/recipe-ingredients', methods=['POST'])
def recipe_ingredients():
    data = request.get_json()
    try:
        recipe_ingredient = RecipeIngredient(
            recipe_id=data['recipe_id'],
            ingredient_id=data['ingredient_id'],
            quantity=data['quantity']
        )
        db.session.add(recipe_ingredient)
        db.session.commit()
        return jsonify(recipe_ingredient.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5556, debug=True)