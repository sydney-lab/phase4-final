import React, { useState, useEffect } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const UserSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, 'Name must be at least 2 characters')
    .matches(/^[A-Za-z\s]+$/, 'Name can only contain letters and spaces')
    .required('Name is required'),
  email: Yup.string()
    .email('Invalid email format')
    .required('Email is required')
});

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

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
      const response = await fetch('/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      });

      if (response.ok) {
        fetchUsers();
        resetForm();
      }
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  return (
    <div>
      <h1>Users</h1>
      
      <div className="form-container">
        <h2>Add New User</h2>
        <Formik
          initialValues={{ name: '', email: '' }}
          validationSchema={UserSchema}
          onSubmit={handleSubmit}
        >
          <Form>
            <div className="form-group">
              <label>Name:</label>
              <Field name="name" type="text" />
              <ErrorMessage name="name" component="div" className="error" />
            </div>

            <div className="form-group">
              <label>Email:</label>
              <Field name="email" type="email" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>

            <button type="submit" className="btn">Add User</button>
          </Form>
        </Formik>
      </div>

      <div>
        <h2>All Users</h2>
        {users.map(user => (
          <div key={user.id} className="recipe-card">
            <h3>{user.name}</h3>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Recipes:</strong> {user.recipes?.length || 0}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Users;