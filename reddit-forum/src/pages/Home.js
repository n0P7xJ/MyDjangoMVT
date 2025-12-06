import React, { useState, useEffect } from 'react';
import PostCard from '../components/PostCard';
import TopicsBar from '../components/TopicsBar';
import { getPosts, votePost } from '../utils/api';
import './Home.css';

function Home() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState(null);

  useEffect(() => {
    loadPosts();
  }, [selectedTopic]);

  const loadPosts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (selectedTopic) {
        params.topic = selectedTopic.slug;
      }
      const response = await getPosts(params);
      setPosts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading posts:', error);
      setLoading(false);
    }
  };

  const handleVote = async (slug, voteType) => {
    try {
      await votePost(slug, voteType);
      loadPosts();
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
  };

  return (
    <>
      <TopicsBar onTopicSelect={handleTopicSelect} selectedTopic={selectedTopic} />
      
      <div className="home-container">
        <div className="main-content">
          <div className="feed-header">
            <h1>{selectedTopic ? selectedTopic.name : 'Популярні пости'}</h1>
            {selectedTopic && selectedTopic.description && (
              <p className="topic-description">{selectedTopic.description}</p>
            )}
          </div>
          
          {loading ? (
            <div className="loading">Завантаження...</div>
          ) : (
            <div className="posts-list">
              {posts.length === 0 ? (
                <div className="no-posts">Постів ще немає. Створіть перший!</div>
              ) : (
                posts.map(post => (
                  <PostCard 
                    key={post.id} 
                    post={post} 
                    onVote={handleVote}
                  />
                ))
              )}
            </div>
          )}
        </div>
        
        <div className="sidebar">
          <div className="sidebar-card">
            <h3>Про спільноту</h3>
            <p>Ласкаво просимо! Це Reddit-подібний форум створений на Django + React.</p>
          </div>
          
          {selectedTopic && (
            <div className="sidebar-card">
              <div className="topic-info">
                {selectedTopic.icon && (
                  <div className="topic-icon-large">{selectedTopic.icon}</div>
                )}
                <h3>{selectedTopic.name}</h3>
                {selectedTopic.description && (
                  <p>{selectedTopic.description}</p>
                )}
                <div className="topic-stats">
                  <div className="stat">
                    <strong>{selectedTopic.communities_count || 0}</strong>
                    <span>спільнот</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default Home;
