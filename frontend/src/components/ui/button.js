import React from 'react';

const variantClasses = {
  default: 'bg-blue-500 text-white hover:bg-blue-600',
  outline: 'border border-blue-500 text-blue-500 hover:bg-blue-50',
  destructive: 'bg-red-500 text-white hover:bg-red-600',
};

export function Button({ children, variant = 'default', size = 'md', className = '', ...props }) {
  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${variantClasses[variant]} ${sizeClasses[size]} rounded ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
