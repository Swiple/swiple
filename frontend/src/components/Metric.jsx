import React from 'react';
import { Statistic } from 'antd';

function MetricCard({ ...props }) {
  return (
    <Statistic
      {...props}
    />
  );
}

export default MetricCard;
