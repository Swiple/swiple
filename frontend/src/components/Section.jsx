import React from 'react';
import PropTypes from 'prop-types';

function Section({ children, ...props }) {
  return (
    <div
      className="section"
      {...props}
    >
      {children}
    </div>
  );
}

Section.propTypes = {
  children: PropTypes.element.isRequired,
};

export default Section;
