import React, { useState, useEffect } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const RecipeSchema = Yup.object().shape({
  title: Yup.string()
    .min(2, 'Title must be at least 2 characters')
    .required('Title is required'),
  instructions: Yup.string()
    .min(10, 'Instructions must be at least 10 characters')
    .required('Instructions are required'),
  cook_time: Yup.number()
    .positive('Cook time must be positive')
    .integer('Cook time must be a whole number')
    .required('Cook time is required'),
  user_id: Yup.number()
    .positive('Please select a user')
    .required('User is required')
});

function Recipes() {
  const [recipes, setRecipes] = useState([]);
  const [users, setUsers] = useState([]);
  const [editingRecipe, setEditingRecipe] = useState(null);

  useEffect(() => {
    fetchRecipes();
    fetchUsers();
  }, []);

  const fetchRecipes = async () => {
    try {
      const response = await fetch('/recipes');
      const data = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch('/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (values, { resetForm }) => {
    try {
      const url = editingRecipe ? `/recipes/${editingRecipe.id}` : '/recipes';
      const method = editingRecipe ? 'PATCH' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        fetchRecipes();
        resetForm();
        setEditingRecipe(null);
      }
    } catch (error) {
      console.error('Error saving recipe:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`/recipes/${id}`, { method: 'DELETE' });
      if (response.ok) {
        fetchRecipes();
      }
    } catch (error) {
      console.error('Error deleting recipe:', error);
    }
  };

  const handleEdit = (recipe) => {
    setEditingRecipe(recipe);
  };

  return (
    <div>
      <h1>Recipes</h1>
      
      <div className="form-container">
        <h2>{editingRecipe ? 'Edit Recipe' : 'Add New Recipe'}</h2>
        <Formik
          initialValues={{
            title: editingRecipe?.title || '',
            instructions: editingRecipe?.instructions || '',
            cook_time: editingRecipe?.cook_time || '',
            user_id: editingRecipe?.user_id || ''
          }}
          validationSchema={RecipeSchema}
          onSubmit={handleSubmit}
          enableReinitialize
        >
          <Form>
            <div className="form-group">
              <label>Title:</label>
              <Field name="title" type="text" />
              <ErrorMessage name="title" component="div" className="error" />
            </div>

            <div className="form-group">
              <label>Instructions:</label>
              <Field name="instructions" as="textarea" rows="4" />
              <ErrorMessage name="instructions" component="div" className="error" />
            </div>

            <div className="form-group">
              <label>Cook Time (minutes):</label>
              <Field name="cook_time" type="number" />
              <ErrorMessage name="cook_time" component="div" className="error" />
            </div>

            <div className="form-group">
              <label>User:</label>
              <Field name="user_id" as="select">
                <option value="">Select a user</option>
                {users.map(user => (
                  <option key={user.id} value={user.id}>{user.name}</option>
                ))}
              </Field>
              <ErrorMessage name="user_id" component="div" className="error" />
            </div>

            <button type="submit" className="btn">
              {editingRecipe ? 'Update Recipe' : 'Add Recipe'}
            </button>
            {editingRecipe && (
              <button type="button" className="btn" onClick={() => setEditingRecipe(null)}>
                Cancel
              </button>
            )}
          </Form>
        </Formik>
      </div>

      <div>
        <h2>All Recipes</h2>
        {recipes.map(recipe => (
          <div key={recipe.id} className="recipe-card">
            <h3>{recipe.title}</h3>
            <p><strong>Cook Time:</strong> {recipe.cook_time} minutes</p>
            <p><strong>Instructions:</strong> {recipe.instructions}</p>
            <p><strong>Created by:</strong> {recipe.user?.name}</p>
            <button className="btn" onClick={() => handleEdit(recipe)}>Edit</button>
            <button className="btn btn-danger" onClick={() => handleDelete(recipe.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recipes;