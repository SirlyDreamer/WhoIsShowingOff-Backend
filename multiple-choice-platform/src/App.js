import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/login';
import Main from './components/main';
import MCQ from './components/questions';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [roomID, setRoomID] = useState('');

  const handleLogin = async (userID, userName) => {
    try {
      const response = await axios.post('http://127.0.0.1:11452/login', { userID, userName });
      if (response.data.status === 0) {
        const user = { userID, userName };
        setUser(user);
        await handleJoinRoom('0000', user);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleJoinRoom = async (roomID, user) => {
    try {
      const response = await axios.post('http://127.0.0.1:11452/join', { roomID, userID: user.userID });
      if (response.data.status === 0) {
        setRoomID(roomID);
      }
    } catch (error) {
      console.error('Join room error:', error);
    }
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={user ? <Navigate to="/main" /> : <Login onLogin={handleLogin} />} />
          <Route path="/main" element={user ? <Main user={user} roomID={roomID} /> : <Navigate to="/" />} />
          <Route path="/questions" element={user && roomID ? <MCQ sseUrl={`http://127.0.0.1:11452/events?roomID=${roomID}`} user={user} roomID={roomID} /> : <Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
