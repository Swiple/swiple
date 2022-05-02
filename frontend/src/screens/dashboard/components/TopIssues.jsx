import React from 'react';
import PropTypes from 'prop-types';
import { Card, Table } from 'antd';
import { Link } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';

function TopIssues({ loading, data }) {
  const columns = [
    {
      title: 'Dataset',
      dataIndex: 'dataset',
      render: (text, record) => (
        <Link to={`/dataset/home?dataset-id=${record.dataset_id}`}>
          {record.dataset_name}
        </Link>
      ),
    },
    {
      title: 'Datasource',
      dataIndex: 'datasource_name',
    },
    {
      title: 'Quality Measure',
      dataIndex: 'rate',
    },
    {
      title: '# Failures',
      dataIndex: '#_failures',
    },
  ];

  return (
    <Card
      loading={loading}
      bordered={false}
      title="Top Issues"
      style={{
        height: '100%',
      }}
    >
      <Table
        size="small"
        columns={columns}
        dataSource={data}
        pagination={{
          style: {
            marginBottom: 0,
          },
          pageSize: 5,
        }}
        rowKey={() => uuidv4()}
      />
    </Card>
  );
}

TopIssues.defaultProps = {
  loading: false,
  data: [],
};

TopIssues.propTypes = {
  loading: PropTypes.bool,
  data: PropTypes.arrayOf(Object),
};

export default TopIssues;
