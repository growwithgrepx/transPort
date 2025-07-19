import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  className = '',
  onClick,
  ...props 
}) => {
  const baseClasses = 'btn-primary';
  const combinedClasses = `${baseClasses} ${className}`.trim();

  const handleKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (onClick) {
        onClick(event as unknown as React.MouseEvent<HTMLButtonElement, MouseEvent>);
      }
    }
  };

  return (
    <button 
      className={combinedClasses}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      {...props}
    >
      {children}
    </button>
  );
}; 