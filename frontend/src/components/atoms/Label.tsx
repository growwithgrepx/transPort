import React from 'react';

type LabelVariant = 'error' | 'success' | 'warning' | string;
type LabelSize = 'small' | 'medium' | 'large';

const variantClasses: Record<string, string> = {
  error: 'text-red-600',
  success: 'text-green-600',
  warning: 'text-yellow-600',
};

interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  children: React.ReactNode;
  variant?: LabelVariant;
  size?: LabelSize;
  required?: boolean;
  requiredText?: string;
}

export const Label: React.FC<LabelProps> = ({ 
  children, 
  variant,
  size = 'medium',
  required = false,
  requiredText = '*',
  className = '',
  ...props 
}) => {
  const baseClasses = 'form-label';
  // Variant classes
  const variantClass = variant ? variantClasses[variant] || '' : '';
  // Size classes
  const sizeClasses = {
    small: 'text-xs',
    medium: 'text-sm',
    large: 'text-base',
  }[size] || 'text-sm';
  const combinedClasses = `${baseClasses} ${variantClass} ${sizeClasses} ${className}`.trim();
  return (
    <label 
      className={combinedClasses}
      {...props}
    >
      {children}
      {required && (
        <span className="text-red-500 ml-1" aria-label="required">
          {requiredText}
        </span>
      )}
    </label>
  );
}; 