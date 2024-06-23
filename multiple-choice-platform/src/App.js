import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/login';
import Main from './components/main';
import Room from './components/Room';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [roomID, setRoomID] = useState('');
  const [question, setQuestion] = useState({ question: '', options: [] });
  const [score, setScore] = useState(0);
  const [phase, setPhase] = useState('login'); // phases: login, main, room
  const [players, setPlayers] = useState([]);
  const [totalQuestions, setTotalQuestions] = useState(0);

  useEffect(() => {
    if (phase === 'room') {
      const source = new EventSource(`http://127.0.0.1:11451/events?roomID=${roomID}`);

      source.addEventListener('start', (event) => {
        const data = JSON.parse(event.data);
        setTotalQuestions(data.total);
        setPlayers(data.players);
        setQuestion(data.question);
        console.log('Start event received:', data);
      });

      source.addEventListener('question', (event) => {
        const data = JSON.parse(event.data);
        setQuestion(data.question);
        console.log('Question event received:', data);
      });

      source.addEventListener('answer', (event) => {
        const data = JSON.parse(event.data);
        console.log('Answer event received:', data);
        // Handle answer event if necessary
      });

      source.addEventListener('timeout', (event) => {
        console.log('Timeout event received');
        // Handle timeout event if necessary
      });

      return () => {
        source.close();
      };
    }
  }, [phase, roomID]);

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

  const handleAnswerOptionClick = async (isCorrect) => {
    if (isCorrect) {
      setScore(score + 1);
    }
    try {
      const response = await axios.post(`http://127.0.0.1:11451/rooms/${roomID}/submit`, { roomID, userID: user.userID, answer: isCorrect });
      if (response.data.status === 0) {
        setQuestion(response.data.nextQuestion);
      }
    } catch (error) {
      console.error('Submit answer error:', error);
    }
  };

  const handleBackToMain = () => {
    setPhase('main');
  };

  return (
    <div className="app">
      {phase === 'login' && <Login onLogin={handleLogin} />}
      {phase === 'main' && <Main user={user} onJoinRoom={handleJoinRoom} />}
      {phase === 'room' && question && (
        <Room
          question={question}
          onOptionClick={handleAnswerOptionClick}
          sseUrl={`http://127.0.0.1:11451/events?roomID=${roomID}`}
          score={score}
          onBackToMain={handleBackToMain}
          user={user}
          roomID={roomID}
        />
      )}
    </div>
  );
};

export default App;
