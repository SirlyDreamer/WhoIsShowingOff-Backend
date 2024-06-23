import React from 'react';
import Option from './Option';

const Question = ({ question, onOptionClick }) => {
  return (
    <div className="question-container">
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
    </div>
  );
};

export default Question;
