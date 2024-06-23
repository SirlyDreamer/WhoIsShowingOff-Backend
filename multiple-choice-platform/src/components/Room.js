import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

const Room = ({ sseUrl, user, roomID, onLeave }) => {
  const [timeLeft, setTimeLeft] = useState(30);
  const [eventSource, setEventSource] = useState(null);
  const [players, setPlayers] = useState([user]);
  const [readyStatus, setReadyStatus] = useState(false);

  useEffect(() => {
    // Create a new EventSource instance
    const source = new EventSource(sseUrl);
    setEventSource(source);


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

    // Clean up on component unmount
    return () => {
      source.close();
    };
  }, [sseUrl]);
  
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
  const handleBackToMain = async () => {
    try {
      await axios.post(`http://127.0.0.1:11451/leave`, { roomID, userID: user.userID });
      onLeave();
    } catch (error) {
      console.error('Error leaving room:', error);
    }
  };
  

  return (
    <div className="room-container">
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
      <button onClick={handleBackToMain}>
        {"leave"}
      </button>
      
    </div>
  );
};

Room.propTypes = {
  sseUrl: PropTypes.string.isRequired,
  user: PropTypes.shape({
    userID: PropTypes.string.isRequired,
  }).isRequired,
  roomID: PropTypes.string.isRequired,
  onLeave: PropTypes.func.isRequired,
};

export default Room;
