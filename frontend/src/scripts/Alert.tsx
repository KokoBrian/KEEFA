import React, { useEffect, useState } from 'react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error';
  duration?: number; // milliseconds before auto-dismiss
  onClose?: () => void; // callback when toast fully closes
}

const Toast: React.FC<ToastProps> = ({
  message,
  type = 'success',
  duration = 4000,
  onClose,
}) => {
  const [visible, setVisible] = useState(true);
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    // Start exit animation after duration
    const timer = setTimeout(() => {
      setExiting(true);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration]);

  useEffect(() => {
    // When exiting animation ends, notify parent to unmount
    if (exiting) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, 300); // match animation duration

      return () => clearTimeout(timer);
    }
  }, [exiting, onClose]);

  if (!visible) return null;

  return (
    <div
      role="alert"
      className={`
        fixed top-5 right-5 z-50 max-w-xs px-6 py-4 rounded shadow-lg font-semibold text-white
        ${
          type === 'success'
            ? 'bg-success-600'
            : 'bg-error-600'
        }
        ${exiting ? 'animate-slide-out-right' : 'animate-slide-in-right'}
        pointer-events-auto
      `}
      style={{ animationDuration: '300ms' }}
    >
      {message}
    </div>
  );
};

export default Toast;
