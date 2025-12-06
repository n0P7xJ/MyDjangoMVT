import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCommunities, createPost } from '../utils/api';
import './CreatePost.css';

function CreatePost() {
  const navigate = useNavigate();
  const [communities, setCommunities] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    post_type: 'text',
    community: '',
    link_url: '',
  });

  useEffect(() => {
    loadCommunities();
  }, []);

  const loadCommunities = async () => {
    try {
      const response = await getCommunities();
      setCommunities(response.data);
      if (response.data.length > 0) {
        setFormData(prev => ({ ...prev, community: response.data[0].id }));
      }
    } catch (error) {
      console.error('Error loading communities:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createPost(formData);
      navigate(`/r/${response.data.community}/post/${response.data.slug}`);
    } catch (error) {
      console.error('Error creating post:', error);
      alert('Помилка при створенні посту');
    }
  };

  return (
    <div className="create-post-page">
      <div className="create-post-container">
        <h1>Створити пост</h1>
        
        <form onSubmit={handleSubmit} className="create-post-form">
          <div className="form-group">
            <label>Оберіть спільноту</label>
            <select 
              name="community" 
              value={formData.community} 
              onChange={handleChange}
              required
            >
              {communities.map(community => (
                <option key={community.id} value={community.id}>
                  r/{community.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Тип посту</label>
            <div className="post-type-tabs">
              <button
                type="button"
                className={formData.post_type === 'text' ? 'active' : ''}
                onClick={() => setFormData({...formData, post_type: 'text'})}
              >
                📝 Текст
              </button>
              <button
                type="button"
                className={formData.post_type === 'link' ? 'active' : ''}
                onClick={() => setFormData({...formData, post_type: 'link'})}
              >
                🔗 Посилання
              </button>
              <button
                type="button"
                className={formData.post_type === 'image' ? 'active' : ''}
                onClick={() => setFormData({...formData, post_type: 'image'})}
              >
                🖼️ Зображення
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Заголовок</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Цікавий заголовок..."
              required
              maxLength="300"
            />
          </div>

          {formData.post_type === 'text' && (
            <div className="form-group">
              <label>Текст (опціонально)</label>
              <textarea
                name="content"
                value={formData.content}
                onChange={handleChange}
                placeholder="Текст (опціонально)"
                rows="10"
              />
            </div>
          )}

          {formData.post_type === 'link' && (
            <div className="form-group">
              <label>URL</label>
              <input
                type="url"
                name="link_url"
                value={formData.link_url}
                onChange={handleChange}
                placeholder="https://..."
                required
              />
            </div>
          )}

          <div className="form-actions">
            <button type="button" onClick={() => navigate('/')} className="btn-cancel">
              Скасувати
            </button>
            <button type="submit" className="btn-submit">
              Опублікувати
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreatePost;
