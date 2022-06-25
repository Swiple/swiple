import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Button, Dropdown, Layout, Menu, message, Modal,
  Row, Table, Typography,
} from 'antd';
import {
  DeleteFilled, EditFilled,
  EllipsisOutlined, ExclamationCircleOutlined, PlusOutlined,
} from '@ant-design/icons';
import moment from 'moment';
import { v4 as uuidv4 } from 'uuid';
import {
  deleteDataSource, getDataSources,
} from '../../Api';
import Section from '../../components/Section';
import DatasourceModal, { CREATE_TYPE, UPDATE_TYPE } from './components/DatasourceModal';
import {
  AthenaIcon, BigqueryIcon, MysqlIcon, PostgresqlIcon, RedshiftIcon, SnowflakeIcon, TrinoIcon,
} from '../../static/images';

const { Content } = Layout;
const { Title } = Typography;
const { confirm } = Modal;

export default function DatasourceOverview() {
  const [datasourceModal, setDatasourceModal] = useState({ visible: false, type: '', dataset: null });

  const [refreshDataSources, setRefreshDataSources] = useState(true);
  const [dataSources, setDataSources] = useState([]);
  const history = useHistory();

  useEffect(() => {
    if (refreshDataSources) {
      getDataSources()
        .then((response) => {
          if (response.status === 200) {
            setDataSources(response.data);
          } else {
            message.error('An error occurred while retrieving data sources.', 5);
          }
          setRefreshDataSources(false);
        });
    }
  }, [history, refreshDataSources, setRefreshDataSources]);

  const openDataSourceModal = (modalType, record = null) => {
    let datasource = null;
    if (modalType === UPDATE_TYPE) {
      [datasource] = dataSources.filter((item) => item.key === record.key);
    }

    setDatasourceModal({
      visible: true, type: modalType, datasource, engine: datasource?.engine,
    });
  };

  const removeDatasource = (row) => new Promise((resolve, reject) => {
    deleteDataSource(row.key).then(() => {
      setDataSources(dataSources.filter((item) => item.key !== row.key));
      resolve();
    }).catch(() => reject());
  });

  const showDeleteModal = (record) => {
    confirm({
      title: 'Delete Datasource',
      icon: <ExclamationCircleOutlined />,
      content: "Deleting a datasource will also remove it's datasets, expectations, and validations.",
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeDatasource(record);
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
        onClick={() => showDeleteModal(record)}
        icon={<DeleteFilled style={{ color: 'red' }} />}
      >
        Delete
      </Menu.Item>
    </Menu>
  );

  const getEngineIcon = (engine) => {
    const datasourceImgMap = {
      postgresql: PostgresqlIcon,
      redshift: RedshiftIcon,
      snowflake: SnowflakeIcon,
      mysql: MysqlIcon,
      bigquery: BigqueryIcon,
      athena: AthenaIcon,
      trino: TrinoIcon,
    };
    return datasourceImgMap[engine.toLowerCase()];
  };

  const columns = [
    {
      title: 'DATA SOURCE',
      dataIndex: 'datasource_name',
    },
    {
      title: 'DATABASE',
      dataIndex: 'database',
    },
    {
      title: 'ENGINE',
      dataIndex: 'engine',
      render: (text) => (
        <img
          style={{ position: 'relative', width: 20, height: 20 }}
          src={getEngineIcon(text)}
          alt={text}
        />
      ),
    },
    {
      title: 'CREATE DATE',
      dataIndex: 'create_date',
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
            icon={<EllipsisOutlined rotate={90} style={{ fontWeight: 'bold', fontSize: '25px' }} />}
          />
        </Dropdown>
      ),
    },
  ];

  const formattedDataSources = () => dataSources.map((item) => ({
    key: item.key,
    datasource_name: item.datasource_name,
    database: item.database,
    engine: item.engine,
    create_date: moment(item.create_date).local().fromNow(),
    modified_date: moment(item.modified_date).local().fromNow(),
  }));

  return (

    <Content className="site-layout-background">
      <Section
        style={{
          margin: '24px 16px',
          padding: 24,
        }}
      >
        <>
          <Typography style={{ paddingLeft: '16px' }}>
            <Row style={{ alignItems: 'center' }} align="space-between">
              <Title
                className="card-list-header"
                level={4}
              >
                Data Sources
              </Title>
              <Button
                className="card-list-button-dark"
                style={{ fontWeight: 'bold' }}
                type="primary"
                icon={<PlusOutlined />}
                size="medium"
                onClick={() => openDataSourceModal(CREATE_TYPE)}
              >
                Data Source
              </Button>
              <DatasourceModal
                visible={datasourceModal.visible}
                type={datasourceModal.type}
                editedDatasource={datasourceModal.datasource}
                engine={datasourceModal.engine}
                onCancel={() => {
                  setDatasourceModal({
                    visible: false, type: '', datasource: null, engine: '',
                  });
                }}
                onFormSubmit={() => {
                  setDatasourceModal({
                    visible: false, type: '', datasource: null, engine: '',
                  });
                  setRefreshDataSources(true);
                }}
              />
            </Row>
          </Typography>
          <Table
            columns={columns}
            dataSource={formattedDataSources()}
            pagination={{ position: ['bottomRight'] }}
            rowKey={() => uuidv4()}
          />
        </>
      </Section>
    </Content>
  );
}
