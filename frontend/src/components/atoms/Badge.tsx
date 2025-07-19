import React from 'react';

type BadgeVariant = 'success' | 'warning' | 'danger' | 'info' | string;
type BadgeSize = 'small' | 'medium' | 'large';
type IconPosition = 'left' | 'right';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  icon?: string;
  iconPosition?: IconPosition;
}

export const Badge: React.FC<BadgeProps> = ({ 
  children, 
  variant,
  size = 'small',
  icon,
  iconPosition = 'left',
  className = '',
  ...props 
}) => {
  const baseClasses = 'badge';
  
  // Variant classes
  const variantClasses = variant ? `badge-${variant}` : '';
  
  // Size classes
  const sizeClasses = {
    small: 'text-xs',
    medium: 'text-sm',
    large: 'text-base',
  }[size] || 'text-xs';
  
  const combinedClasses = `${baseClasses} ${variantClasses} ${sizeClasses} ${className}`.trim();

  const renderIcon = () => {
    if (!icon) return null;
    return <span className="mr-1">{icon}</span>;
  };

  const renderContent = () => {
    if (!icon) return children;
    
    if (iconPosition === 'right') {
      return (
        <>
          {children}
          <span className="ml-1">{icon}</span>
        </>
      );
    }
    
    return (
      <>
        {renderIcon()}
        {children}
      </>
    );
  };

  return (
    <span 
      className={combinedClasses}
      {...props}
    >
      {renderContent()}
    </span>
  );
}; 