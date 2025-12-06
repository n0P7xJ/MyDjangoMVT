import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Topics
export const getTopics = (params) => api.get('/forum/topics/', { params });
export const getTopic = (slug) => api.get(`/forum/topics/${slug}/`);
export const getTopicCommunities = (slug) => api.get(`/forum/topics/${slug}/communities/`);

// Communities
export const getCommunities = () => api.get('/forum/communities/');
export const getCommunity = (slug) => api.get(`/forum/communities/${slug}/`);
export const createCommunity = (data) => api.post('/forum/communities/', data);
export const joinCommunity = (slug) => api.post(`/forum/communities/${slug}/join/`);
export const leaveCommunity = (slug) => api.post(`/forum/communities/${slug}/leave/`);

// Posts
export const getPosts = (params) => api.get('/forum/posts/', { params });
export const getPost = (slug) => api.get(`/forum/posts/${slug}/`);
export const createPost = (data) => api.post('/forum/posts/', data);
export const votePost = (slug, voteType) => api.post(`/forum/posts/${slug}/vote/`, { vote_type: voteType });
export const unvotePost = (slug) => api.delete(`/forum/posts/${slug}/unvote/`);

// Comments
export const getComments = (postSlug) => api.get(`/forum/posts/${postSlug}/comments/`);
export const createComment = (data) => api.post('/forum/comments/', data);
export const voteComment = (id, voteType) => api.post(`/forum/comments/${id}/vote/`, { vote_type: voteType });
export const getReplies = (id) => api.get(`/forum/comments/${id}/replies/`);

export default api;
