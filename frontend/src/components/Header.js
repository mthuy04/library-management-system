import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css'; // Chúng ta sẽ tạo file này để trang trí sau

function Header() {
  return (
    <header className="app-header">
      <Link to="/" className="logo">
        LibraryApp
      </Link>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </nav>
    </header>
  );
}

// Dòng này CỰC KỲ QUAN TRỌNG, nó cho phép file khác import component này
export default Header;