import React, { useState, useEffect } from 'react';
import { getTopics } from '../utils/api';
import './TopicsBar.css';

function TopicsBar({ onTopicSelect, selectedTopic }) {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTopics();
  }, []);

  const loadTopics = async () => {
    try {
      // Завантажуємо тільки головні теми (parent=null)
      const response = await getTopics({ parent: 'null' });
      setTopics(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading topics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="topics-bar">Завантаження...</div>;
  }

  return (
    <div className="topics-bar">
      <div className="topics-container">
        <button
          className={`topic-btn ${!selectedTopic ? 'active' : ''}`}
          onClick={() => onTopicSelect(null)}
        >
          <span className="topic-icon">🏠</span>
          <span className="topic-name">Головна</span>
        </button>

        {topics.map(topic => (
          <button
            key={topic.id}
            className={`topic-btn ${selectedTopic?.id === topic.id ? 'active' : ''}`}
            onClick={() => onTopicSelect(topic)}
            style={{ '--topic-color': topic.color }}
          >
            {topic.icon && <span className="topic-icon">{topic.icon}</span>}
            <span className="topic-name">{topic.name}</span>
            {topic.communities_count > 0 && (
              <span className="topic-badge">{topic.communities_count}</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

export default TopicsBar;
