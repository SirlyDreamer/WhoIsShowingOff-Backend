import React, { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';

const Login = ({ onLogin }) => {
  const [userID, setUserID] = useState('');
  const [userName, setUserName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(userID, userName);
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Typography variant="h4" gutterBottom>准备装逼?</Typography>
      <form onSubmit={handleSubmit}>
        <TextField label="User ID" value={userID} onChange={(e) => setUserID(e.target.value)} margin="normal" fullWidth />
        <TextField label="User Name" value={userName} onChange={(e) => setUserName(e.target.value)} margin="normal" fullWidth />
        <Button type="submit" variant="contained" color="primary">Login</Button>
      </form>
    </Box>
  );
};

export default Login;
