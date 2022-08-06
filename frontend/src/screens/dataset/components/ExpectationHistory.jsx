import React from 'react';
import ReactECharts from 'echarts-for-react';
import PropTypes from 'prop-types';
import moment from 'moment';

const formatter = Intl.NumberFormat('en', { notation: 'compact' });

function ExpectationHistory({ validations, resultType }) {
  const percentageValue = (row) => {
    const color = row.success ? '#38C438' : '#F54646';
    let resultValue;

    if (resultType === 'column_map_expectation') {
      resultValue = Number((100 - row.result.unexpected_percent).toFixed(5));
    } else if (resultType === 'column_aggregate_expectation' || resultType === 'expectation') {
      resultValue = Number(row.result.observed_value).toFixed(5);
    } else {
      throw Error(`${resultType} not implemented. Data`);
    }
    return {
      value: [row.run_date, resultValue],
      itemStyle: {
        color,
      },
    };
  };

  const objectiveValue = (row) => {
    if (!row.expectation_config.kwargs.objective) return null;
    return row.expectation_config.kwargs.objective * 100;
  };

  const formatResults = () => {
    const values = {
      percentageValues: [],
      objectiveValues: [],
    };

    if (!validations) {
      return values;
    }

    for (let i = 0; i < validations.length; i += 1) {
      values.percentageValues.push(
        percentageValue(validations[i]),
      );
      values.objectiveValues.push(
        [validations[i].run_date, objectiveValue(validations[i])],
      );
    }
    return values;
  };

  const { percentageValues, objectiveValues } = formatResults();

  const abbreviateNumber = (value) => formatter.format(value);

  const objectiveMarkLineData = () => {
    if (objectiveValues.length > 0 && objectiveValues[objectiveValues.length - 1][1] !== null) {
      return [{
        name: 'Obj.',
        yAxis: [objectiveValues[objectiveValues.length - 1][1]],
        label: {
          position: 'start',
          show: true,
          formatter: '{b} {c}%',
        },
      }];
    }
    return [];
  };
  let yAxis;
  if (resultType === 'column_map_expectation') {
    yAxis = {
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
        scale: true,
      },
    };
  } else if (resultType === 'column_aggregate_expectation' || resultType === 'expectation') {
    yAxis = {
      yAxis: {
        type: 'value',
        position: 'right',
        axisLabel: {
          formatter(value) {
            return abbreviateNumber(value);
          },
        },
        axisLine: {
          show: true,
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        scale: true,
        splitNumber: 2,
      },
    };
  } else {
    throw Error(`${resultType} not implemented`);
  }

  const options = {
    tooltip: {
      trigger: 'axis',
      position(pt, params, dom, rect, size) {
        const xCoord = pt[0] - size.contentSize[0] / 2;
        return [xCoord, '-90%'];
      },
    },
    grid: {
      top: 5,
      right: 40,
      bottom: 5,
      left: 53,
    },
    xAxis: {
      type: 'time',
      boundaryGap: false,
      axisLine: {
        show: false,
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
      min: moment().subtract(7, 'd').toISOString(),
      max: moment().toISOString(),
    },
    ...yAxis,
    series: [
      {
        labelLine: {
          show: true,
        },
        name: 'Objective',
        silent: true,
        data: objectiveValues,
        type: 'line',
        color: '#A7A7A7FF',
        symbol: 'none',
        lineStyle: {
          type: 'dashed',
          width: 1,
        },
      },
      {
        name: 'Pass Rate',
        type: 'line',
        data: percentageValues,
        color: '#333',
        markLine: {
          name: 'Obj.',
          symbol: ['none', 'none'],
          label: {
            position: 'start',
            fontSize: 10,
            fontWeight: 'bold',
          },
          data: objectiveMarkLineData(),
          lineStyle: {
            color: 'transparent',
          },
        },
      },
    ],
    animation: false,
  };

  return (
    <ReactECharts
      style={{ height: 100, minWidth: 350 }}
      option={options}
    />
  );
}

ExpectationHistory.propTypes = {
  validations: PropTypes.arrayOf(Object).isRequired,
  resultType: PropTypes.string.isRequired,
};

export default ExpectationHistory;
