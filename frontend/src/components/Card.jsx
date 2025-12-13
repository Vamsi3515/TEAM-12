import React from 'react';

const Card = ({ 
  children, 
  className = '', 
  hover = false,
  padding = 'md',
  shadow = true,
  onClick,
  ...props
}) => {
  const paddingSizes = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const baseStyles = `bg-white rounded-xl border border-slate-200 transition-all duration-300 ${
    shadow ? 'shadow-soft' : ''
  } ${hover ? 'hover:shadow-xl hover:scale-[1.02] cursor-pointer' : ''}`;

  return (
    <div 
      className={`${baseStyles} ${paddingSizes[padding]} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
