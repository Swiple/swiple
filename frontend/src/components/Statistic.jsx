import React from 'react';
import { Statistic as AntDStatistic } from 'antd';

function Statistic({ ...props }) {
  return (
    <AntDStatistic
      {...props}
      valueStyle={{ fontSize: '30px' }}
    />
  );
}

export default Statistic;
