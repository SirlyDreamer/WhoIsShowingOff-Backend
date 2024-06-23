import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Option from './Option';

const Room = ({ question, onOptionClick, sseUrl, user, roomID, onBackToMain }) => {
  const [eventSource, setEventSource] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(question);
  const [players, setPlayers] = useState([]);
  const [readyStatus, setReadyStatus] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  const [timeLeft, setTimeLeft] = useState(30);

  useEffect(() => {
    const fetchRoomDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:11451/rooms/${roomID}`);
        if (response.data.owner === user.userID) {
          setIsOwner(true);
        }
      } catch (error) {
        console.error('Error fetching room details:', error);
      }
    };

    fetchRoomDetails();

    // Create a new EventSource instance
    const source = new EventSource(sseUrl);
    setEventSource(source);

    // Listen for 'timer' events
    source.addEventListener('timer', (event) => {
      const data = JSON.parse(event.data);
      setTimeLeft(data.timeLeft);
    });

    // Listen for 'start' events to reset the timer and set a new question
    source.addEventListener('start', (event) => {
      const data = JSON.parse(event.data);
      setTimeLeft(30); // Reset timer to 30 seconds
      setCurrentQuestion(data.question); // Set the new question
    });

    // Listen for 'join' events to update the list of players
    source.addEventListener('join', (event) => {
      const data = JSON.parse(event.data);
      setPlayers((prevPlayers) => [...prevPlayers, { userID: data.userID, ready: false }]);
    });

    // Listen for 'ready' events to update ready status of players
    source.addEventListener('ready', (event) => {
      const data = JSON.parse(event.data);
      setPlayers((prevPlayers) =>
        prevPlayers.map((player) =>
          player.userID === data.userID ? { ...player, ready: true } : player
        )
      );
    });

    // Listen for 'deready' events to update ready status of players
    source.addEventListener('deready', (event) => {
      const data = JSON.parse(event.data);
      setPlayers((prevPlayers) =>
        prevPlayers.map((player) =>
          player.userID === data.userID ? { ...player, ready: false } : player
        )
      );
    });

    // Listen for 'leave' events to remove the player from the list
    source.addEventListener('leave', (event) => {
      const data = JSON.parse(event.data);
      setPlayers((prevPlayers) =>
        prevPlayers.filter((player) => player.userID !== data.userID)
      );
    });

    // Clean up on component unmount
    return () => {
      source.close();
    };
  }, [sseUrl, roomID, user.userID]);

  const handleGetReady = async () => {
    if (!user || !user.userID) {
      console.error('User information is missing.');
      return;
    }
    try {
      if (readyStatus) {
        await axios.post(`http://127.0.0.1:11451/rooms/${roomID}/deready`, { userID: user.userID });
        setReadyStatus(false);
      } else {
        await axios.post(`http://127.0.0.1:11451/rooms/${roomID}/ready`, { userID: user.userID });
        setReadyStatus(true);
      }
    } catch (error) {
      console.error('Error changing ready status:', error);
    }
  };

  const handleLeaveRoom = async () => {
    try {
      await axios.post(`http://127.0.0.1:11451/leave`, { roomID, userID: user.userID });
      onBackToMain();
    } catch (error) {
      console.error('Error leaving room:', error);
    }
  };

  const handleStartGame = async () => {
    try {
      await axios.post(`http://127.0.0.1:11451/rooms/${roomID}/start`, { userID: user.userID });
    } catch (error) {
      console.error('Error starting game:', error);
    }
  };

  return (
    <div className="room-container">
      <h2>{currentQuestion.question}</h2>
      <div className="options">
        {currentQuestion.options.map((option, index) => (
          <Option key={index} option={option} onOptionClick={onOptionClick} />
        ))}
      </div>
      <div className="countdown-bar">
        <div className="countdown" style={{ width: `${(timeLeft / 30) * 100}%` }}></div>
      </div>
      <div className="players-list">
        <h3>Players:</h3>
        <ul>
          {players.map((player) => (
            <li key={player.userID}>
              {player.userID} {player.ready ? '(Ready)' : ''}
            </li>
          ))}
        </ul>
      </div>
      <button onClick={handleGetReady}>
        {readyStatus ? 'De-Ready' : 'Get Ready'}
      </button>
      <button onClick={handleLeaveRoom}>Leave Room</button>
      {isOwner && <button onClick={handleStartGame}>Start Game</button>}
    </div>
  );
};

export default Room;
