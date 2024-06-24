import React, { useEffect } from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Main = ({ user, roomID }) => {
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the room ID is '0000' and navigate to questions
    if (roomID === '0000') {
      navigate('/questions');
    }

    // Create a new EventSource instance for start signal
    const eventSource = new EventSource(`http://127.0.0.1:11451/start-signal?roomID=${roomID}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.start) {
        navigate('/questions');
      }
    };

    return () => {
      eventSource.close();
    };
  }, [navigate, roomID]);

  const handleStart = async () => {
    try {
      await axios.post(`http://127.0.0.1:11451/rooms/${roomID}/start`, { userID: user.userID });
    } catch (error) {
      console.error('Error starting the game:', error);
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Typography variant="h4" gutterBottom>Welcome, {user.userName}</Typography>
      <Typography variant="h6">Waiting for the admin to start the quiz...</Typography>
      <Typography variant="h6">Go here to practice</Typography>
      {user.userName === 'admin' && (
        <Button variant="contained" color="primary" onClick={handleStart}>
          Start Game
        </Button>
      )}
    </Box>
  );
};

export default Main;
