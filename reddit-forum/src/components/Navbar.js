import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">🔴</span>
          <span className="logo-text">reddit</span>
        </Link>
        
        <div className="navbar-search">
          <input 
            type="text" 
            placeholder="Пошук..." 
            className="search-input"
          />
        </div>
        
        <div className="navbar-actions">
          <Link to="/submit" className="btn-create-post">
            <span>+ Створити пост</span>
          </Link>
          <button className="btn-login">Увійти</button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
