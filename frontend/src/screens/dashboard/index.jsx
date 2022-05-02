import React, { useEffect, useState } from 'react';
import {
  Layout, message,
} from 'antd';
import { withRouter } from 'react-router-dom';
import { getDashboardIssues, getDashboardMetrics } from '../../Api';
import TopIssues from './components/TopIssues';
import IntroduceRow from './components/IntroduceRow';

const { Content } = Layout;

const Dashboard = withRouter(() => {
  const [loading, setLoading] = useState({
    topIssues: false,
    metricData: false,
    dashboardMetrics: false,
  });
  const [fetchDashboardMetrics, setFetchDashboardMetrics] = useState(true);
  const [topIssues, setTopIssues] = useState(null);
  const [metricData, setMetricData] = useState({});

  useEffect(() => {
    if (fetchDashboardMetrics) {
      setLoading((prevState) => ({
        ...prevState,
        dashboardMetrics: true,
      }));
      getDashboardMetrics()
        .then((response) => {
          if (response.status === 200) {
            console.log(response.data);
            setMetricData(response.data);
          } else {
            message.error('An error occurred while retrieving data sources schema.', 5);
          }
          setLoading((prevState) => ({
            ...prevState,
            dashboardMetrics: false,
          }));
          setFetchDashboardMetrics(false);
        });
    }
  }, [fetchDashboardMetrics]);

  useEffect(() => {
    if (topIssues === null) {
      setLoading((prevState) => ({
        ...prevState,
        topIssues: true,
      }));
      getDashboardIssues()
        .then((response) => {
          if (response.status === 200) {
            setTopIssues(response.data);
          } else {
            message.error('An error occurred while retrieving Validation Statistics.', 5);
          }
          setLoading((prevState) => ({
            ...prevState,
            topIssues: false,
          }));
        });
    }
  }, [topIssues, setTopIssues]);

  // Visuals we want
  // Datasets ordered by those with lowest DQ (link)
  // Upcoming schedules
  // Expectation runs that failed
  // Asset counts (datasource, schema, dataset, expectations)
  // Dataset coverage ?
  // Recently added datasets

  return (
    <Content className="site-layout-background card-list">
      <div
        style={{
          margin: '24px 16px',
          background: 'transparent',
        }}
      >
        <IntroduceRow
          loading={loading.metricData}
          datasource={metricData.datasource}
          dataset={metricData.dataset}
          expectation={metricData.expectation}
          validation={metricData.validation}
        />
        <TopIssues
          loading={loading.topIssues}
          data={topIssues}
        />
      </div>
    </Content>
  );
});

export default Dashboard;
