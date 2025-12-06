import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import PostCard from '../components/PostCard';
import { getCommunity, getPosts, votePost } from '../utils/api';
import './CommunityPage.css';

function CommunityPage() {
  const { slug } = useParams();
  const [community, setCommunity] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCommunity();
    loadPosts();
  }, [slug]);

  const loadCommunity = async () => {
    try {
      const response = await getCommunity(slug);
      setCommunity(response.data);
    } catch (error) {
      console.error('Error loading community:', error);
    }
  };

  const loadPosts = async () => {
    try {
      const response = await getPosts({ community: slug });
      setPosts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading posts:', error);
      setLoading(false);
    }
  };

  const handleVote = async (postSlug, voteType) => {
    try {
      await votePost(postSlug, voteType);
      loadPosts();
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  if (loading || !community) {
    return <div className="loading">Завантаження...</div>;
  }

  return (
    <div className="community-page">
      <div className="community-header">
        <div className="community-banner">
          {community.banner && <img src={community.banner} alt={community.name} />}
        </div>
        <div className="community-info">
          <h1>r/{community.name}</h1>
          <p>{community.description}</p>
          <div className="community-stats">
            <span>{community.members_count} учасників</span>
          </div>
        </div>
      </div>

      <div className="community-content">
        <div className="posts-section">
          {posts.map(post => (
            <PostCard key={post.id} post={post} onVote={handleVote} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default CommunityPage;
