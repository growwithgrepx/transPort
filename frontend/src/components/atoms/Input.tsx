import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export const Input: React.FC<InputProps> = ({ 
  label,
  id,
  className = '',
  ...props 
}) => {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  const baseClasses = 'form-input';
  const combinedClasses = `${baseClasses} ${className}`.trim();

  return (
    <div>
      {label && (
        <label htmlFor={inputId} className="form-label">
          {label}
        </label>
      )}
      <input 
        id={inputId}
        className={combinedClasses}
        {...props}
      />
    </div>
  );
}; 