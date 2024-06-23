import React, { useState } from 'react';

const Main = ({ user, onJoinRoom }) => {
  const [roomID, setRoomID] = useState('');

  const handleJoinRoom = () => {
    onJoinRoom(roomID);
  };

  return (
    <div>
      <h1>Main</h1>
      <p>Welcome, {user.userName}</p>
      <div className="input-container">
        <input type="text" placeholder="Room ID" value={roomID} onChange={(e) => setRoomID(e.target.value)} />
      </div>
      <div className="button-container">
        <button onClick={handleJoinRoom}>Join/Create Room</button>
      </div>
    </div>
  );
};

export default Main;
