import React from 'react';
import { Table } from 'antd';
import PropTypes from 'prop-types';
import { v4 as uuidv4 } from 'uuid';

function DataSample({ columns, rows }) {
  const datasetSample = () => {
    if (Object.keys(rows).length > 0) {
      const columnsList = columns.map((column) => ({
        title: column,
        dataIndex: column,
        ellipsis: true,
      }));
      return (
        <Table
          pagination={false}
          pageSize={10}
          scroll={{ x: true }}
          columns={columnsList}
          dataSource={rows}
          rowKey={() => uuidv4()}
          tableLayout="-"
        />
      );
    }
    return null;
  };
  return (
    <>
      {datasetSample()}
    </>
  );
}

DataSample.propTypes = {
  columns: PropTypes.arrayOf(Object).isRequired,
  rows: PropTypes.arrayOf(Object).isRequired,
};

export default DataSample;
