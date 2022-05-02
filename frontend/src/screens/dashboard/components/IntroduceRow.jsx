import React from 'react';
import {
  Row, Col,
} from 'antd';
import ReactECharts from 'echarts-for-react';
import PropTypes from 'prop-types';
import ChartCard from './ChartCard';

function IntroduceRow({
  loading,
  datasource,
  dataset,
  expectation,
  validation,
}) {
  const topColResponsiveProps = {
    xs: 24,
    sm: 12,
    md: 12,
    lg: 12,
    xl: 6,
    style: {
      marginBottom: 24,
    },
  };

  const simpleBarChart = (color, points) => {
    const options = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      color,
      grid: {
        top: 5,
        right: 0,
        bottom: 0,
        left: 5,
      },
      xAxis: {
        type: 'time',
        show: false,
      },
      yAxis: {
        type: 'value',
        show: false,
        axisLine: {
          show: false,
        },
      },
      series: [
        {
          data: points,
          type: 'bar',
        },
      ],
    };
    return (
      <ReactECharts style={{ height: 80, width: '100%' }} option={options} />
    );
  };

  return (
    <Row gutter={24}>
      <Col {...topColResponsiveProps}>
        <ChartCard
          bordered={false}
          loading={loading}
          title="Datasources"
          total={datasource?.count}
          contentHeight={80}
        >
          {simpleBarChart('#1990FF', datasource?.points)}
        </ChartCard>
      </Col>
      <Col {...topColResponsiveProps}>
        <ChartCard
          bordered={false}
          loading={loading}
          title="Datasets"
          total={dataset?.count}
          contentHeight={80}
        >
          {simpleBarChart('#1990FF', dataset?.points)}
        </ChartCard>
      </Col>
      <Col {...topColResponsiveProps}>
        <ChartCard
          bordered={false}
          loading={loading}
          title="Expectations"
          total={expectation?.count}
          contentHeight={80}
        >
          {simpleBarChart('#1990FF', expectation?.points)}
        </ChartCard>
      </Col>
      <Col {...topColResponsiveProps}>
        <ChartCard
          bordered={false}
          loading={loading}
          title="Validations"
          total={validation?.count}
          contentHeight={80}
        >
          {simpleBarChart('#1990FF', validation?.points)}
        </ChartCard>
      </Col>
    </Row>
  );
}

const metricShape = PropTypes.shape({
  count: PropTypes.number,
  points: PropTypes.arrayOf(Object),
});

const defaultMetric = {
  count: null,
  points: [],
};

IntroduceRow.defaultProps = {
  loading: false,
  datasource: defaultMetric,
  schema: defaultMetric,
  dataset: defaultMetric,
  expectation: defaultMetric,
  validation: defaultMetric,
};

IntroduceRow.propTypes = {
  loading: PropTypes.bool,
  datasource: metricShape,
  schema: metricShape,
  dataset: metricShape,
  expectation: metricShape,
  validation: metricShape,
};

export default IntroduceRow;
