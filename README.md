# Phase 4 Final Project - Recipe Management System

A full-stack web application built with Flask backend and React frontend for managing recipes, users, and ingredients.

## Features

### Backend (Flask)
- **Models**: User, Recipe, Ingredient, RecipeIngredient (join table)
- **Relationships**: 
  - User → Recipes (one-to-many)
  - Recipe ↔ Ingredients (many-to-many with quantity attribute)
- **API Routes**: Full CRUD for recipes, Create/Read for users and ingredients
- **CORS enabled** for client-server communication

### Frontend (React)
- **3 Routes**: Home, Recipes, Users
- **Navigation bar** for route switching
- **Form validation** on all inputs
- **Validations**: 
  - Data type validation (numbers, emails)
  - String format validation (name patterns, email format)
  - Required field validation

## Setup Instructions

### Backend Setup
1. Navigate to server directory:
   ```bash
   cd server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. Seed database:
   ```bash
   python3 seed.py
   ```

5. Run Flask server:
   ```bash
   python3 app.py
   # Server will run on http://localhost:5556
   ```

### Frontend Setup
1. Navigate to client directory:
   ```bash
   cd client
   ```

2. Open the React app in your browser:
   ```bash
   # Open index.html in any web browser
   open index.html
   # OR double-click the index.html file
   ```

## Project Requirements Met

✅ Flask API backend with React frontend  
✅ 3+ models (User, Recipe, Ingredient, RecipeIngredient)  
✅ 2+ one-to-many relationships (User→Recipes)  
✅ 1 many-to-many relationship with user submittable attribute (Recipe↔Ingredients with quantity)  
✅ Full CRUD for recipes  
✅ Create/Read for all resources  
✅ Form validation with error handling  
✅ Data type validation (numbers, emails)  
✅ String/format validation (name patterns, email format)  
✅ 3+ client-side routes with navigation  
✅ Client-server communication via fetch()  
✅ CORS implementation  
✅ Proper HTTP status codes