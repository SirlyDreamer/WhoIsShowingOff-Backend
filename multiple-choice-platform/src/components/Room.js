import React, { useState, useEffect } from 'react';
import Option from './Option';

const Room = ({ question, onOptionClick }) => {
  const [timeLeft, setTimeLeft] = useState(30);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      onOptionClick(false); // Automatically handle timeout as a wrong answer
    }
  }, [timeLeft, onOptionClick]);

  return (
    <div className="room-container">
      <h2>{question.question}</h2>
      <div className="options">
        {question.options.map((option, index) => (
          <Option
            key={index}
            option={option}
            onOptionClick={onOptionClick}
          />
        ))}
      </div>
      <div className="countdown-bar">
        <div
          className="countdown"
          style={{ width: `${(timeLeft / 30) * 100}%` }}
        ></div>
      </div>
    </div>
  );
};

export default Room;
