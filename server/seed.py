from app import app, db, User, Recipe, Ingredient, RecipeIngredient

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create users
    user1 = User(name="John Doe", email="john@example.com")
    user2 = User(name="Jane Smith", email="jane@example.com")
    
    # Create ingredients
    flour = Ingredient(name="Flour")
    sugar = Ingredient(name="Sugar")
    eggs = Ingredient(name="Eggs")
    butter = Ingredient(name="Butter")
    
    db.session.add_all([user1, user2, flour, sugar, eggs, butter])
    db.session.commit()
    
    # Create recipes
    recipe1 = Recipe(
        title="Chocolate Cake",
        instructions="Mix ingredients and bake at 350F for 30 minutes",
        cook_time=30,
        user_id=user1.id
    )
    
    recipe2 = Recipe(
        title="Sugar Cookies",
        instructions="Mix, roll, cut, and bake at 375F for 12 minutes",
        cook_time=12,
        user_id=user2.id
    )
    
    db.session.add_all([recipe1, recipe2])
    db.session.commit()
    
    # Create recipe ingredients
    ri1 = RecipeIngredient(recipe_id=recipe1.id, ingredient_id=flour.id, quantity="2 cups")
    ri2 = RecipeIngredient(recipe_id=recipe1.id, ingredient_id=sugar.id, quantity="1 cup")
    ri3 = RecipeIngredient(recipe_id=recipe2.id, ingredient_id=flour.id, quantity="3 cups")
    ri4 = RecipeIngredient(recipe_id=recipe2.id, ingredient_id=butter.id, quantity="1/2 cup")
    
    db.session.add_all([ri1, ri2, ri3, ri4])
    db.session.commit()
    
    print("Database seeded successfully!")