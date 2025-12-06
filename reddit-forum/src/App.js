import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import TopicsBar from './components/TopicsBar';
import Home from './pages/Home';
import CommunityPage from './pages/CommunityPage';
import PostPage from './pages/PostPage';
import CreatePost from './pages/CreatePost';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/r/:slug" element={<CommunityPage />} />
          <Route path="/r/:communitySlug/post/:postSlug" element={<PostPage />} />
          <Route path="/submit" element={<CreatePost />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
