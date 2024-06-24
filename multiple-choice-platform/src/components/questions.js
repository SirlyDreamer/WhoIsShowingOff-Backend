import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MCQ.css'; // Import the CSS file

const MCQ = ({ sseUrl, user, roomID }) => {
  const [question, setQuestion] = useState('');
  const [choices, setChoices] = useState([]);
  const [selectedChoice, setSelectedChoice] = useState(null);

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:11452/rooms/${roomID}/question`);
        const data = response.data;
        setQuestion(data.question || '');
        setChoices([
          data.short_answer,
          data.wrong_answer_1,
          data.wrong_answer_2,
          data.wrong_answer_3,
          data.wrong_answer_4,
          data.wrong_answer_5
        ]);
      } catch (error) {
        console.error('Error fetching question:', error);
      }
    };

    fetchQuestion();
  }, [roomID]);

  const handleSubmit = async () => {
    try {
      await axios.post(`http://127.0.0.1:11452/rooms/${roomID}/submit`, {
        userID: user.userID,
        answer: selectedChoice,
      });
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      handleSubmit();
    }, 6000);

    return () => {
      clearTimeout(timer);
    };
  }, [selectedChoice]);

  return (
    <div className="mcq-container">
      <h2>{question}</h2>
      <ul className="choices-list">
        {choices.map((choice, index) => (
          <li key={index} className="choice-item">
            <label>
              <input
                type="radio"
                name="choice"
                value={choice}
                onChange={() => setSelectedChoice(choice)}
              />
              {choice}
            </label>
          </li>
        ))}
      </ul>
      <button className="submit-button" onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default MCQ;
