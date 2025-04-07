// frontend/src/components/StyleOptions.js
import React from 'react';

const StyleOptions = ({ tone, setTone, length, setLength, style, setStyle }) => {
  const options = {
    tone: [
      { value: 'default', label: 'Default' },
      { value: 'professional', label: 'Professional' },
      { value: 'conversational', label: 'Conversational' },
      { value: 'witty', label: 'Witty' },
      { value: 'enthusiastic', label: 'Enthusiastic' }
    ],
    length: [
      { value: 'medium', label: 'Medium' },
      { value: 'short', label: 'Short' },
      { value: 'long', label: 'Long' }
    ],
    style: [
      { value: 'standard', label: 'Standard' },
      { value: 'storytelling', label: 'Storytelling' },
      { value: 'minimalistic', label: 'Minimalistic' },
      { value: 'technical', label: 'Technical' }
    ]
  };

  const handleChange = (setter) => (e) => setter(e.target.value);

  const renderSelect = (label, value, setter, optionsArray) => (
    <>
      <label className="block font-semibold">{label}</label>
      <select 
        className="w-full border px-2 py-1 rounded" 
        value={value} 
        onChange={handleChange(setter)}
      >
        {optionsArray.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </>
  );

  return (
    <div className="space-y-2 mt-4">
      {renderSelect('Tone', tone, setTone, options.tone)}
      {renderSelect('Length', length, setLength, options.length)}
      {renderSelect('Style', style, setStyle, options.style)}
    </div>
  );
};

export default StyleOptions;