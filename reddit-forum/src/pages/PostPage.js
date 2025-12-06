import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getPost, getComments, votePost, createComment } from '../utils/api';
import './PostPage.css';

function PostPage() {
  const { postSlug } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPost();
    loadComments();
  }, [postSlug]);

  const loadPost = async () => {
    try {
      const response = await getPost(postSlug);
      setPost(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading post:', error);
      setLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const response = await getComments(postSlug);
      setComments(response.data);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  };

  const handleVote = async (voteType) => {
    try {
      await votePost(postSlug, voteType);
      loadPost();
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    try {
      await createComment({
        content: commentText,
        post: post.id,
      });
      setCommentText('');
      loadComments();
    } catch (error) {
      console.error('Error creating comment:', error);
    }
  };

  if (loading || !post) {
    return <div className="loading">Завантаження...</div>;
  }

  return (
    <div className="post-page">
      <div className="post-container">
        <div className="post-detail">
          <div className="vote-section-vertical">
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
          
          <div className="post-main">
            <div className="post-header">
              <span className="community">r/{post.community.name}</span>
              <span className="dot">•</span>
              <span className="author">Posted by u/{post.author.username}</span>
            </div>
            
            <h1 className="post-title">{post.title}</h1>
            
            {post.image && (
              <div className="post-image">
                <img src={post.image} alt={post.title} />
              </div>
            )}
            
            {post.content && (
              <div className="post-content">
                <p>{post.content}</p>
              </div>
            )}
          </div>
        </div>

        <div className="comments-section">
          <h3>Коментарі ({post.comments_count})</h3>
          
          <form className="comment-form" onSubmit={handleSubmitComment}>
            <textarea
              placeholder="Що ви думаєте?"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              rows="4"
            />
            <button type="submit">Коментувати</button>
          </form>

          <div className="comments-list">
            {comments.map(comment => (
              <div key={comment.id} className="comment">
                <div className="comment-header">
                  <strong>{comment.author.username}</strong>
                  <span className="comment-time">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="comment-content">{comment.content}</p>
                <div className="comment-actions">
                  <span className="comment-score">↑ {comment.score}</span>
                  <button className="reply-btn">Відповісти</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PostPage;
