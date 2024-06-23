import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/login';
import Main from './components/main';
import Room from './components/Room';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [roomID, setRoomID] = useState('');
  const [phase, setPhase] = useState('login'); // phases: login, main, room

  const handleLogin = async (userID, userName) => {
    try {
      const response = await axios.post('http://127.0.0.1:11451/login', { userID, userName });
      if (response.data.status === 0) {
        setUser({ userID, userName });
        setPhase('main');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleJoinRoom = async (roomID, user) => {
    try {
      const response = await axios.post('http://127.0.0.1:11451/join', { roomID, userID: user.userID });
      if (response.data.status === 0) {
        setRoomID(roomID);
        setPhase('room');
      }
    } catch (error) {
      console.error('Join room error:', error);
    }
  };

  const handleLeaveRoom = () => {
    setPhase('main');
    setRoomID('');
  };

  return (
    <div className="app">
      {phase === 'login' && <Login onLogin={handleLogin} />}
      {phase === 'main' && <Main user={user} onJoinRoom={handleJoinRoom} />}
      {phase === 'room' && (
        <Room
          sseUrl={`http://127.0.0.1:11451/events?roomID=${roomID}`}
          user={user}
          roomID={roomID}
          onLeave={handleLeaveRoom}
        />
      )}
    </div>
  );
};

export default App;
