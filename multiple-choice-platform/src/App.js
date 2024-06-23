import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/login';
import Main from './components/main';
import Room from './components/Room';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [roomID, setRoomID] = useState('');
  const [question, setQuestion] = useState(null);
  const [score, setScore] = useState(0);
  const [phase, setPhase] = useState('login'); // phases: login, main, room

  const handleLogin = async (userID, userName) => {
    try {
      const response = await axios.post('/login', { userID, userName });
      if (response.data.status === 0) {
        setUser({ userID, userName });
        setPhase('main');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleJoinRoom = async (roomID) => {
    try {
      const response = await axios.post('/join', { roomID, userID: user.userID });
      if (response.data.status === 0) {
        setRoomID(roomID);
        setQuestion(response.data.question);
        setPhase('room');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleAnswerOptionClick = async (isCorrect) => {
    if (isCorrect) {
      setScore(score + 1);
    }
    try {
      const response = await axios.post('/answer', { roomID, userID: user.userID, answer: isCorrect });
      setQuestion(response.data.nextQuestion);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="app">
      {phase === 'login' && <Login onLogin={handleLogin} />}
      {phase === 'main' && <Main user={user} onJoinRoom={handleJoinRoom} />}
      {phase === 'room' && question && (
        <Room question={question} onOptionClick={handleAnswerOptionClick} score={score} />
      )}
    </div>
  );
};

export default App;
