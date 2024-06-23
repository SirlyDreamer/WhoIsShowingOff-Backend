import React, { useState } from 'react';

const Main = ({ user, onJoinRoom }) => {
  const [roomID, setRoomID] = useState('');

  const handleJoinRoom = () => {
    onJoinRoom(roomID, user);
  };

  return (
    <div>
      <h1>到底是谁在装逼？</h1>
      <p>Welcome, {user.userName}</p>
      <div className="input-container">
        <input
          type="text"
          placeholder="Room ID (Enter any text, will join dummy room)"
          value={roomID}
          onChange={(e) => setRoomID(e.target.value)}
        />
      </div>
      <div className="button-container">
        <button onClick={handleJoinRoom}>Join/Create Room</button>
      </div>
    </div>
  );
};

export default Main;
