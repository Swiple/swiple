import React, { useEffect, useState } from 'react';
import { Link, withRouter } from 'react-router-dom';
import {
  Button, Dropdown, Layout, Menu, message, Modal,
  Row, Table, Typography,
} from 'antd';
import {
  DeleteFilled,
  EditFilled, EllipsisOutlined, ExclamationCircleOutlined,
  PlusOutlined, TableOutlined,
} from '@ant-design/icons';
import moment from 'moment';
import { v4 as uuidv4 } from 'uuid';
import {
  deleteDataset, getDatasets,
} from '../../Api';
import Section from '../../components/Section';
import DatasetModal, { CREATE_TYPE, UPDATE_TYPE } from './components/DatasetModal';
import { splitDatasetResource } from '../../Utils';

const { Content } = Layout;
const { Title } = Typography;
const { confirm } = Modal;

const DatasetOverview = withRouter(() => {
  const [datasetModal, setDatasetModal] = useState({ visible: false, type: '', dataset: null });
  const [refreshDatasets, setRefreshDataset] = useState(true);
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    if (refreshDatasets) {
      getDatasets()
        .then((response) => {
          if (response.status === 200) {
            setDatasets(response.data);
          } else {
            message.error('An error occurred while retrieving datasetsList.', 5);
          }
          setRefreshDataset(false);
        });
    }
  }, [refreshDatasets, setRefreshDataset]);

  const openDataSourceModal = (modalType, record = null) => {
    let dataset = null;
    if (modalType === UPDATE_TYPE) {
      [dataset] = datasets.filter((item) => item.key === record.key);
    }

    setDatasetModal({ visible: true, type: modalType, dataset });
  };

  const removeDataset = (row) => new Promise((resolve, reject) => {
    deleteDataset(row.key).then(() => {
      setDatasets(datasets.filter((item) => item.key !== row.key));
      resolve();
    }).catch(() => reject());
  });

  const showDeleteDatasetModal = (record) => {
    confirm({
      title: 'Delete Dataset',
      icon: <ExclamationCircleOutlined />,
      content: "Deleting a dataset will also remove it's expectations and validations.",
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeDataset(record);
      },
      onCancel() {},
    });
  };

  const actionMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openDataSourceModal(UPDATE_TYPE, record)}
      >
        Edit
      </Menu.Item>
      <Menu.Item
        key="2"
        onClick={() => showDeleteDatasetModal(record)}
        icon={<DeleteFilled style={{ color: 'red' }} />}
      >
        Delete
      </Menu.Item>
    </Menu>
  );

  const getTableColumns = () => [
    {
      title: 'NAME',
      dataIndex: 'dataset_name',
      render: (text, record) => (
        <Link
          key={2}
          to={{
            pathname: '/dataset/home',
            search: `?dataset-id=${record.key}`,
            state: { dataset: record },
          }}
        >
          <Row justify="start" align="middle">
            <TableOutlined
              key={1}
              className="table-icon"
              style={{
                fontSize: 22,
                marginRight: 16,
                color: record.is_virtual ? '#1890FF' : 'rgba(0,0,0,.85)',
              }}
            />
            {text}
          </Row>
        </Link>
      ),
    },
    {
      title: 'DATASOURCE',
      dataIndex: 'datasource',
    },
    {
      title: 'SCHEMA',
      dataIndex: 'schema',
    },
    {
      title: 'LAST MODIFIED',
      dataIndex: 'modified_date',
    },
    {
      title: '',
      dataIndex: 'action',
      render: (text, record) => (
        <Dropdown
          trigger={['click']}
          overlay={actionMenu(record)}
          placement="bottomRight"
          arrow
        >
          <Button
            type="text"
            icon={(
              <EllipsisOutlined
                rotate={90}
                style={{ fontWeight: 'bold', fontSize: '25px' }}
              />
            )}
          />
        </Dropdown>
      ),
    },
  ];

  const datasetsList = datasets.map((item) => {
    const { datasetSchema, datasetName, isVirtual } = splitDatasetResource(item);
    return {
      key: item.key,
      is_virtual: isVirtual,
      dataset_name: datasetName,
      schema: datasetSchema,
      datasource: item.datasource_name,
      database: item.database,
      create_date: moment(item.create_date).local().fromNow(),
      modified_date: moment(item.modified_date).local().fromNow(),
    };
  });

  return (
    <Content className="site-layout-background card-list">
      <Section
        style={{
          margin: '24px 16px',
          padding: 24,
        }}
      >
        <div>
          <Typography style={{ paddingLeft: '16px' }}>
            <Row style={{ alignItems: 'center' }} align="space-between">
              <Title className="card-list-header" level={4}>Datasets</Title>
              <Button
                className="card-list-button-dark"
                style={{ fontWeight: 'bold' }}
                type="primary"
                icon={<PlusOutlined />}
                size="medium"
                onClick={() => openDataSourceModal(CREATE_TYPE)}
              >
                Dataset
              </Button>
              <DatasetModal
                visible={datasetModal.visible}
                type={datasetModal.type}
                editedDataset={datasetModal.dataset}
                onCancel={() => {
                  setDatasetModal({ visible: false, type: '', dataset: null });
                }}
                onFormSubmit={() => {
                  setDatasetModal({ visible: false, type: '', dataset: null });
                  setRefreshDataset(true);
                }}
              />
            </Row>
          </Typography>
          <Table
            columns={getTableColumns()}
            dataSource={datasetsList}
            pagination={{ position: ['bottomRight'] }}
            rowKey={() => uuidv4()}
          />
        </div>
      </Section>
    </Content>
  );
});

export default DatasetOverview;
