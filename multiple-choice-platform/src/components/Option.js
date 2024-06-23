import React from 'react';

const Option = ({ option, onOptionClick }) => {
  return (
    <button
      className="option-button"
      onClick={() => onOptionClick(option.isCorrect)}
    >
      {option.text}
    </button>
  );
};

export default Option;
