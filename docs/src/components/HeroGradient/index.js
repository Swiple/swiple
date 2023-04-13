import React from 'react';
import './styles.module.css';
import clsx from "clsx";
import styles from './styles.module.css';

const HeroGradient = () => {
  return (
    <div
      className={clsx(styles.gradientOuter)}
    >
      <div
        className={clsx(styles.gradient)}
      />
    </div>
  )
};

export default HeroGradient;
