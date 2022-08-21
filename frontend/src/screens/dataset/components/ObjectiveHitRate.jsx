import { Row, Space, Statistic } from 'antd';
import ReactECharts from 'echarts-for-react';
import React from 'react';
import PropTypes from 'prop-types';

function ObjectiveHitRate({ stats }) {
  const validationsDataset = () => {
    if (stats.validations) {
      return stats.validations;
    }
    return [];
  };

  const options = {
    tooltip: {
      trigger: 'axis',
      position(pt, params, dom, rect, size) {
        const xCoord = pt[0] - size.contentSize[0] / 2;
        return [xCoord, '-160%'];
      },
    },
    grid: {
      top: 5,
      right: 40,
      bottom: 5,
      left: 5,
    },
    dataset: {
      source: validationsDataset(),
      dimensions: ['timestamp', 'Pass Rate'],
    },
    xAxis: {
      type: 'time',
      axisLine: {
        show: true,
      },
      axisLabel: {
        show: false,
      },
      splitLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
    },
    yAxis: {
      type: 'value',
      position: 'right',
      axisLabel: {
        formatter: '{value}%',
      },
      axisLine: {
        show: true,
      },
      min: 0,
      max: 100,
      interval: 100,
      splitLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
    },
    series: [
      {
        name: 'Pass Rate',
        type: 'line',
        encode: {
          x: 'timestamp',
          y: 'Pass Rate',
        },
        color: '#333',
        showSymbol: true,
        areaStyle: {
          color: '#FAFAFA',
        },
      },
    ],
  };

  const oneDayAvg = stats['1_day_avg'];
  const sevenDayAvg = stats['7_day_avg'];
  const thirtyOneDayAvg = stats['31_day_avg'];

  return (
    <Row justify="start" style={{ paddingBottom: 20 }}>
      <Space size="large">
        <Statistic
          suffix={oneDayAvg ? '%' : null}
          title="Daily Pass Rate"
          value={oneDayAvg ? oneDayAvg.toFixed(0) : '-'}
        />
        <Statistic
          suffix={sevenDayAvg ? '%' : null}
          title="Weekly Pass Rate"
          value={sevenDayAvg ? sevenDayAvg.toFixed(0) : '-'}
        />
        <Statistic
          suffix={thirtyOneDayAvg ? '%' : null}
          title="Monthly Pass Rate"
          value={thirtyOneDayAvg ? thirtyOneDayAvg.toFixed(0) : '-'}
        />
        <div className="ant-statistic">
          <div className="ant-statistic-title">Pass rate over the last month</div>
          <ReactECharts style={{ height: 43, width: 300 }} option={options} />
        </div>
      </Space>
    </Row>
  );
}

ObjectiveHitRate.propTypes = {
  stats: PropTypes.shape({
    '1_day_avg': PropTypes.number,
    '7_day_avg': PropTypes.number,
    '31_day_avg': PropTypes.number,
    validations: PropTypes.arrayOf(Object),
  }).isRequired,
};

export default ObjectiveHitRate;
