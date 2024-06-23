import React, { useState } from 'react';

const Login = ({ onLogin }) => {
  const [userID, setUserID] = useState('');
  const [userName, setUserName] = useState('');

  const handleLogin = () => {
    onLogin(userID, userName);
  };

  return (
    <div>
      <h1>是谁在装逼？</h1>
      <div className="input-container">
        <input type="text" placeholder="User ID" value={userID} onChange={(e) => setUserID(e.target.value)} />
        <input type="text" placeholder="User Name" value={userName} onChange={(e) => setUserName(e.target.value)} />
      </div>
      <div className="button-container">
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
};

export default Login;
