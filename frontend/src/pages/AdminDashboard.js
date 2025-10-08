import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const [books, setBooks] = useState([]);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchBooks = async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/books/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setBooks(res.data);
      } catch (err) {
        console.error(err);
        if (err.response && err.response.status === 403) {
          alert('You do not have admin access.');
          navigate('/profile');
        }
      }
    };
    fetchBooks();
  }, [navigate, token]);

  const handleDelete = async (bookId) => {
    try {
      await axios.delete(`http://localhost:5000/api/books/${bookId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBooks(books.filter(book => book.id !== bookId));
      alert('Book deleted successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to delete book.');
    }
  };

  return (
    <div className="admin-dashboard-container">
      <h2>Admin Dashboard: Book Management</h2>
      <button>Add New Book</button>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.map(book => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.isbn}</td>
              <td>
                <button onClick={() => handleDelete(book.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;