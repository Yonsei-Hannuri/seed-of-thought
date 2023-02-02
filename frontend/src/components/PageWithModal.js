import React, { useState } from 'react';

export default function PageWithModal({
  main,
  modal,
  modalContainerStyle,
  modalBodyStyle,
}) {
  const [modalShow, setModalShow] = useState(false);
  const onToggleModal = () => {
    setModalShow(!modalShow);
  };
  return (
    <div>
      {main(onToggleModal)}
      <div
        style={{
          ...modalContainerStyleDefault,
          ...modalContainerStyle,
          display: modalShow ? '' : 'none',
        }}
      >
        <div style={{ ...modalBodyStyleDefault, ...modalBodyStyle }}>
          {modal(onToggleModal)}
        </div>
      </div>
    </div>
  );
}

const modalContainerStyleDefault = {
  position: 'absolute',
  top: 0,
  left: 0,
  overflow: 'auto',
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.4)',
  zIndex: 1000,
};

const modalBodyStyleDefault = {
  display: 'flex',
  position: 'absolute',
  top: '50%',
  left: '50%',
  overflow: 'auto',
  width: 'calc(90vw)',
  maxWidth: '700px',
  textAlign: 'center',
  backgroundColor: 'rgb(255, 255, 255)',
  borderRadius: '10px',
  boxShadow: '0 2px 3px 0 rgba(34, 36, 38, 0.15)',
  transform: 'translateX(-50%) translateY(-50%)',
};
