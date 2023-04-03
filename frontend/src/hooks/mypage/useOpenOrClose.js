import { useState } from 'react';

/**
 *
 * @param {boolean} defaultOpen
 * @returns {{
 *  isOpen: boolean;
 *  toggle: () => void;
 * }}
 */
const useOpenOrClose = (defaultOpen) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const toggle = () => {
    setIsOpen(!isOpen);
  };
  return {
    isOpen,
    toggle,
  };
};

export default useOpenOrClose;
