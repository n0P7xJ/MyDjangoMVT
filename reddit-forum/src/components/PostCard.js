import React from 'react';
import { Link } from 'react-router-dom';
import './PostCard.css';

function PostCard({ post, onVote }) {
  const handleVote = (voteType) => {
    if (onVote) {
      onVote(post.slug, voteType);
    }
  };

  return (
    <div className="post-card">
      <div className="vote-section">
        <button 
          className={`vote-btn ${post.user_vote === 1 ? 'upvoted' : ''}`}
          onClick={() => handleVote(1)}
        >
          ▲
        </button>
        <span className="vote-score">{post.score}</span>
        <button 
          className={`vote-btn ${post.user_vote === -1 ? 'downvoted' : ''}`}
          onClick={() => handleVote(-1)}
        >
          ▼
        </button>
      </div>
      
      <div className="post-content">
        {post.image && (
          <div className="post-thumbnail">
            <img src={post.image} alt={post.title} />
          </div>
        )}
        
        <div className="post-details">
          <div className="post-meta">
            <Link to={`/r/${post.community}`} className="community-link">
              r/{post.community}
            </Link>
            <span className="dot">•</span>
            <span className="post-author">Posted by u/{post.author.username}</span>
            <span className="dot">•</span>
            <span className="post-time">{new Date(post.created_at).toLocaleDateString()}</span>
          </div>
          
          <Link to={`/r/${post.community}/post/${post.slug}`} className="post-title-link">
            <h2 className="post-title">{post.title}</h2>
          </Link>
          
          {post.content && (
            <p className="post-excerpt">
              {post.content.substring(0, 200)}{post.content.length > 200 ? '...' : ''}
            </p>
          )}
          
          <div className="post-footer">
            <Link to={`/r/${post.community}/post/${post.slug}`} className="comments-link">
              💬 {post.comments_count} коментарів
            </Link>
            <button className="action-btn">Поділитися</button>
            <button className="action-btn">Зберегти</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PostCard;
