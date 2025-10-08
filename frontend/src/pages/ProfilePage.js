import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './ProfilePage.css';

const ProfilePage = () => {
  const [user, setUser] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/auth/profile', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUser(res.data);
      } catch (err) {
        console.error(err);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };
    fetchProfile();
  }, [navigate, token]);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', user.username);
    formData.append('email', user.email);
    if (selectedFile) {
      formData.append('avatar', selectedFile);
    }

    try {
      const res = await axios.put('http://localhost:5000/api/auth/update-profile', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`
        }
      });
      setUser(res.data);
      alert('Profile updated successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to update profile.');
    }
  };

  if (!user.username) {
    return <div>Loading...</div>;
  }

  const avatarSrc = `http://localhost:5000${user.avatar_url}`;

  return (
    <div className="profile-container">
      <h2>My Profile</h2>
      <form onSubmit={handleUpdate}>
        <div className="avatar-section">
          <img src={avatarSrc} alt="User Avatar" className="profile-avatar" />
          <input type="file" onChange={handleFileChange} />
        </div>
        <div>
          <label>Username:</label>
          <input type="text" value={user.username} onChange={(e) => setUser({...user, username: e.target.value})} />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" value={user.email} onChange={(e) => setUser({...user, email: e.target.value})} />
        </div>
        <button type="submit">Update Profile</button>
      </form>
    </div>
  );
};

export default ProfilePage;