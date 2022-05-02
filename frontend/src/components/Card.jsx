import React from 'react';
import { Card as AntDCard } from 'antd';
import PropTypes from 'prop-types';

function Card({ title, children }) {
  return (
    <AntDCard
      title={title}
      bordered={false}
      style={{
        width: 'fit-content',
        backgroundColor: '#FFFFFF',
        borderRadius: '8px',
      }}
    >
      {children}
    </AntDCard>
  );
}

Card.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.arrayOf(Object).isRequired,
};

export default Card;
