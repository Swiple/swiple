import React from 'react';
import { Modal as AntDModal } from 'antd';
import PropTypes from 'prop-types';

function Modal(props) {
  const { children } = props;
  return (
    <AntDModal
      {...props}
      wrapClassName="wrapper-class"
      style={{ top: '50px' }}
      bodyStyle={{
        minWidth: '400px',
        maxHeight: 'calc(100vh - 210px)',
        overflowWrap: 'break-word',
        overflow: 'auto',
      }}
    >
      { children }
    </AntDModal>
  );
}

Modal.defaultProps = {
  children: null,
};

Modal.propTypes = {
  children: PropTypes.node,
};

export default Modal;
