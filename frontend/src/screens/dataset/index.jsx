import React, { useEffect, useState } from 'react';
import { useLocation, withRouter, useHistory } from 'react-router-dom';
import {
  Breadcrumb,
  Button,
  Col,
  Divider,
  Layout,
  message,
  Modal,
  Row,
  Skeleton,
  Space,
  Table,
  Tabs,
  Tag,
  Tooltip,
  Typography,
  Dropdown,
  Menu,
  PageHeader,
  Descriptions,
} from 'antd';
import {
  DeleteFilled, EditFilled, PlusOutlined, ExclamationCircleTwoTone,
  EllipsisOutlined, ExclamationCircleOutlined, SyncOutlined, DatabaseOutlined, TableOutlined,
  CopyOutlined, AppstoreOutlined,
} from '@ant-design/icons';
import moment from 'moment';
import { v4 as uuidv4 } from 'uuid';
import Paragraph from 'antd/es/typography/Paragraph';
import {
  deleteExpectation,
  getDataset, getDataSource,
  getSuggestions,
  deleteSuggestion,
  enableSuggestion,
  getExpectations,
  getValidationStats,
  postRunnerValidateDataset,
  postRunnerProfileDataset,
  putSample,
  getQuerySample,
  getSchedulesForDataset,
  deleteSchedule,
} from '../../Api';
import Section from '../../components/Section';
import CodeEditor from './components/CodeEditor';
import ExpectationHistory from './components/ExpectationHistory';
import SLAHitRate from './components/SLAHitRate';
import DataSample from './components/DataSample';
import AsyncButton from '../../components/AsyncButton';
import ExpectationModal, { CREATE_TYPE, UPDATE_TYPE } from './components/ExpectationModal';
import ScheduleModal from './components/ScheduleModal';
import { splitDatasetResource, getEngineIcon } from '../../Utils';

const { Content } = Layout;
const { Text } = Typography;
const { TabPane } = Tabs;
const { confirm } = Modal;

// A custom hook that builds on useLocation to parse
// the query string for you.
function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const Dataset = withRouter(() => {
  const [refreshDataset, setRefreshDataset] = useState(true);
  const [dataset, setDataset] = useState({});
  const [refreshDatasource, setRefreshDatasource] = useState(true);
  const [datasource, setDatasource] = useState({});
  const [refreshSuggestions, setRefreshSuggestions] = useState(true);
  const [suggestions, setSuggestions] = useState([]);
  const [refreshExpectations, setRefreshExpectations] = useState(true);
  const [expectations, setExpectations] = useState([]);
  const [refreshSchedules, setRefreshSchedules] = useState(true);
  const [schedules, setSchedules] = useState([]);
  const [requestInProgress, setRequestInProgress] = useState(false);
  const [validationStats, setValidationStats] = useState({});
  const [refreshValidationStats, setRefreshValidationStats] = useState(true);
  const [activeTab, setActiveTab] = useState('1');

  const [expectationModal, setExpectationModal] = useState({ visible: false, type: '', dataset: null });
  const [scheduleModal, setScheduleModal] = useState({ visible: false, type: '', editedSchedule: null });

  const history = useHistory();

  const query = useQuery();
  const datasetId = query.get('dataset-id');

  if (!datasetId) {
    history.push('/datasets/home');
  }

  const { datasetSchema, datasetName, isVirtual } = splitDatasetResource(dataset);

  const ignoredProps = ['catch_exceptions', 'include_config', 'result_format'];

  useEffect(() => {
    if (refreshDatasource && dataset.datasource_id) {
      getDataSource(dataset.datasource_id)
        .then((response) => {
          if (response.status === 200) {
            setDatasource(response.data);
          } else {
            message.error('An error occurred while retrieving data source.', 5);
          }
          setRefreshDatasource(false);
        });
    }
  }, [refreshDatasource, setRefreshDatasource, dataset.datasource_id]);

  useEffect(() => {
    if (refreshDataset && datasetId) {
      getDataset(datasetId)
        .then((response) => {
          if (response.status === 200) {
            setDataset(response.data);
          } else if (response.status === 404) {
            message.error('Dataset does not exist.', 2)
              .then(() => history.push('/datasets/home'));
          } else {
            message.error('An error occurred while retrieving dataset.', 5);
          }
          setRefreshDataset(false);
        });
    }
  }, [refreshDataset, setRefreshDataset, datasetId]);

  useEffect(() => {
    if (refreshSchedules && datasetId) {
      getSchedulesForDataset(datasetId)
        .then((response) => {
          if (response.status === 200) {
            setSchedules(response.data);
          } else {
            message.error('An error occurred while retrieving schedules.', 5);
          }
          setRefreshSchedules(false);
        });
    }
  }, [refreshSchedules, setRefreshSchedules, datasetId]);

  useEffect(() => {
    if (refreshExpectations && datasetId) {
      setRequestInProgress(true);
      getExpectations(datasetId, true)
        .then((response) => {
          if (response.status === 200) {
            setExpectations(response.data);
          } else {
            message.error('An error occurred while retrieving expectations.', 5);
          }
          setRefreshExpectations(false);
          setRequestInProgress(false);
        });
    }
  }, [refreshExpectations, setRefreshExpectations, datasetId]);

  useEffect(() => {
    if (refreshSuggestions && datasetId) {
      setRequestInProgress(true);
      getSuggestions(datasetId, true)
        .then((response) => {
          if (response.status === 200) {
            setSuggestions(response.data);
          } else {
            message.error('An error occurred while retrieving suggestions.', 5);
          }
          setRefreshSuggestions(false);
          setRequestInProgress(false);
        });
    }
  }, [refreshSuggestions, setRefreshSuggestions, datasetId]);

  useEffect(() => {
    if (refreshValidationStats && datasetId) {
      setRequestInProgress(true);
      getValidationStats(datasetId, true)
        .then((response) => {
          if (response.status === 200) {
            setValidationStats(response.data);
          } else {
            message.error('An error occurred while retrieving Validation Statistics.', 5);
          }
          setRefreshValidationStats(false);
          setRequestInProgress(false);
        });
    }
  }, [setRefreshExpectations, refreshValidationStats, datasetId]);

  const refreshSample = () => new Promise((resolve, reject) => {
    const datasetCopy = JSON.parse(JSON.stringify(dataset));
    delete datasetCopy.key;
    delete datasetCopy.sample;

    putSample(dataset.key).then((putSampleResponse) => {
      if (putSampleResponse.status === 200) {
        getQuerySample(datasetCopy).then((getSampleResponse) => {
          if (getSampleResponse.status === 200) {
            setDataset({
              ...dataset,
              sample: getSampleResponse.data,
            });
          }
          resolve();
        });
      } else {
        resolve();
      }
    }).catch(() => reject());
  });

  const openExpectationModal = (modalType, record = null) => {
    let expectation;
    if (modalType === UPDATE_TYPE) {
      [expectation] = expectations.filter((item) => item.key === record.key);
    }
    setExpectationModal({
      visible: true, type: modalType, expectation, dataset,
    });
  };

  const openScheduleModal = (modalType, record = null) => {
    let schedule;
    if (modalType === UPDATE_TYPE) {
      [schedule] = schedules.filter((item) => item.id === record.id);
    }
    setScheduleModal({
      visible: true, type: modalType, schedule, trigger: schedule?.trigger?.trigger,
    });
  };

  const rejectSuggestion = (record) => new Promise((resolve) => {
    deleteSuggestion(record.key).then(() => {
      setSuggestions(suggestions.filter((item) => item.key !== record.key));
      resolve();
    });
  });

  const suggestionsColumns = [
    {
      title: 'NAME',
      dataIndex: 'expectation_type',
    },
    {
      title: 'DOCUMENTATION',
      dataIndex: 'documentation',
      render: (text) => (
        <p className="expectation-documentation">
          {text}
        </p>
      ),
    },
    {
      title: '',
      dataIndex: 'action',
      render: (text, record) => (
        <Row style={{ flexFlow: 'row nowrap' }}>
          <Space>
            <AsyncButton
              style={{ fontWeight: 'bold' }}
              size="medium"
              onClick={() => rejectSuggestion(record)}
            >
              Reject
            </AsyncButton>
            <AsyncButton
              style={{ fontWeight: 'bold' }}
              type="primary"
              size="medium"
              ghost
              onClick={() => new Promise((resolve, reject) => {
                enableSuggestion(record.key).then((response) => {
                  if (response.status === 200) {
                    setSuggestions(suggestions.filter((item) => item.key !== record.key));
                    setRefreshExpectations(true);
                    resolve();
                  }
                }).catch(() => reject());
              })}
            >
              Enable
            </AsyncButton>
          </Space>
        </Row>
      ),
    },
  ];

  const removeExpectation = (record) => new Promise((resolve, reject) => {
    deleteExpectation(record.key).then(() => {
      setRefreshValidationStats(true);
      setExpectations(expectations.filter((item) => item.key !== record.key));
      resolve();
    }).catch(() => reject());
  });

  const showExpectationDeleteModal = (record) => {
    confirm({
      title: 'Delete Expectation',
      icon: <ExclamationCircleOutlined />,
      content: "Deleting an expectation will also remove it's validations.",
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeExpectation(record);
      },
      onCancel() {
      },
    });
  };

  const expectationActionMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openExpectationModal(UPDATE_TYPE, record)}
      >
        Edit
      </Menu.Item>
      <Menu.Item
        key="2"
        onClick={() => showExpectationDeleteModal(record)}
        icon={<DeleteFilled style={{ color: 'red' }} />}
      >
        Delete
      </Menu.Item>
    </Menu>
  );

  const removeSchedule = (record) => new Promise((resolve, reject) => {
    deleteSchedule(record.id).then(() => {
      setSchedules(schedules.filter((item) => item.id !== record.id));
      resolve();
    }).catch(() => reject());
  });

  const showScheduleDeleteModal = (record) => {
    confirm({
      title: 'Delete Schedule',
      icon: <ExclamationCircleOutlined />,
      content: 'Are you sure you want to delete this schedule?',
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeSchedule(record);
      },
      onCancel() {
      },
    });
  };
  const scheduleActionMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openScheduleModal(UPDATE_TYPE, record)}
      >
        Edit
      </Menu.Item>
      <Menu.Item
        key="2"
        onClick={() => showScheduleDeleteModal(record)}
        icon={<DeleteFilled style={{ color: 'red' }} />}
      >
        Delete
      </Menu.Item>
    </Menu>
  );

  const columns = [
    {
      title: 'NAME',
      dataIndex: 'expectation_type',
    },
    {
      title: 'STATUS',
      dataIndex: 'status',
      render: (text, record) => {
        const vLength = record.validations.length;
        if (vLength === 0) return null;
        const lastValidation = record.validations[vLength - 1];

        if (lastValidation?.exception_info.raised_exception === true) {
          return (
            <Tooltip title={`Error running expectation - ${lastValidation.exception_info.exception_message}`}>
              <ExclamationCircleTwoTone twoToneColor="#ff4d4f" style={{ fontSize: 18 }} />
            </Tooltip>
          );
        }
        return lastValidation.success === true ? <Tag color="success">Passed</Tag> : <Tag color="error">Failed</Tag>;
      },
    },
    {
      title: 'HISTORY',
      dataIndex: 'history',
      width: 400,
      render: (text, record) => {
        if (activeTab === '1') {
          return (
            <ExpectationHistory
              validations={record.validations}
              resultType={record.resultType}
            />
          );
        }
        return null;
      },
    },
    {
      title: 'DOCUMENTATION',
      dataIndex: 'documentation',
      render: (text) => (
        <p className="expectation-documentation">
          {text}
        </p>
      ),
    },
    {
      title: '',
      dataIndex: 'action',
      render: (text, record) => (
        <Dropdown
          trigger={['click']}
          overlay={() => expectationActionMenu(record)}
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

  const scheduleColumns = [
    {
      title: 'SCHEDULE TYPE',
      dataIndex: 'trigger',
      render: (record) => (
        record.trigger
      ),
    },
    {
      title: 'EXPRESSION',
      dataIndex: 'expression',
    },
    {
      title: 'MISFIRE GRACE TIME',
      dataIndex: 'misfire_grace_time',
    },
    {
      title: 'MAX INSTANCES',
      dataIndex: 'max_instances',
    },
    {
      title: 'NEXT RUN TIME',
      dataIndex: 'next_run_time',
      render: (text) => (
        moment(text).local().format('ddd, D MMM YYYY HH:mm:ss Z')
      ),
    },
    {
      title: '',
      dataIndex: 'action',
      render: (text, record) => (
        <Dropdown
          trigger={['click']}
          overlay={() => scheduleActionMenu(record)}
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

  const suggestionsList = suggestions.map((suggestion) => ({
    key: suggestion.key,
    expectation_type: suggestion.expectation_type,
    documentation: suggestion.documentation,
    kwargs: suggestion.kwargs,
    create_date: moment(suggestion.create_date).local().fromNow(),
  }));

  const expectationsList = expectations.map((item) => {
    const args = Object.keys(item.kwargs).map((property) => {
      const kwargValue = item.kwargs[property];
      if (!ignoredProps.includes(property) && (kwargValue !== undefined || kwargValue !== null)) {
        return (
          <div key={property}>
            {property}
            :
            {' '}
            {JSON.stringify(kwargValue)}
          </div>
        );
      }
      return null;
    });
    return {
      key: item.key,
      expectation_type: item.expectation_type,
      validations: item.validations,
      documentation: item.documentation,
      arguments: args,
      resultType: item.result_type,
      create_date: moment(item.create_date).local().fromNow(),
      modified_date: moment(item.modified_date).local().fromNow(),
    };
  });

  const analyzeDataset = () => new Promise((resolve) => {
    const data = { datasource_id: datasource.key, dataset_id: datasetId };
    postRunnerValidateDataset(data).then(() => {
      setRefreshValidationStats(true);
      setRefreshExpectations(true);
      resolve();
    });
  });

  const profileDataset = () => new Promise((resolve) => {
    const data = { datasource_id: datasource.key, dataset_id: datasetId };
    setSuggestions([]);
    postRunnerProfileDataset(data).then(() => {
      setRefreshSuggestions(true);
      resolve();
    });
  });

  const tabBarActions = (
    <Space>
      {
        activeTab === '1'
          ? (
            <>
              <Button
                className="card-list-button-dark"
                style={{ fontWeight: 'bold' }}
                type="primary"
                icon={<PlusOutlined />}
                size="medium"
                onClick={() => openExpectationModal(CREATE_TYPE)}
              >
                Expectation
              </Button>
              <AsyncButton
                style={{ fontWeight: 'bold' }}
                type="primary"
                size="medium"
                onClick={() => analyzeDataset()}
                disabled={expectations.length === 0}
              >
                Run Expectations
              </AsyncButton>
            </>
          )
          : null
      }
      {
        activeTab === '2'
          ? (
            <AsyncButton
              className="card-list-button-dark"
              style={{ fontWeight: 'bold' }}
              type="primary"
              icon={<SyncOutlined />}
              size="medium"
              onClick={() => refreshSample()}
            >
              Refresh Sample
            </AsyncButton>
          )
          : null
      }
      {
        activeTab === '4'
          ? (
            <AsyncButton
              style={{ fontWeight: 'bold' }}
              type="primary"
              size="medium"
              onClick={() => profileDataset()}
            >
              Generate Suggestions
            </AsyncButton>
          )
          : null
      }
      {
        activeTab === '5'
          ? (
            <Button
              className="card-list-button-dark"
              style={{ fontWeight: 'bold' }}
              type="primary"
              icon={<PlusOutlined />}
              size="medium"
              onClick={() => openScheduleModal(CREATE_TYPE)}
            >
              Schedule
            </Button>
          )
          : null
      }
    </Space>
  );

  const datasetMetaData = (column = 2) => (
    <Descriptions size="small" column={column}>
      <Descriptions.Item label="Created by">{dataset.created_by}</Descriptions.Item>
      {
        dataset.description
          ? (
            <Paragraph>
              {dataset.description}
            </Paragraph>
          )
          : null
      }
    </Descriptions>
  );

  const breadcrumbs = (
    <Breadcrumb separator="">
      <Breadcrumb.Item>
        {datasource.engine
          ? (
            <>
              <img
                style={{
                  position: 'relative',
                  width: 20,
                  height: 20,
                  marginRight: 8,
                }}
                src={getEngineIcon(datasource.engine)}
                alt={datasource.engine}
              />
              <Text style={{ fontSize: 16, whiteSpace: 'normal' }}>
                {datasource.engine}
              </Text>
            </>
          )
          : <Skeleton.Input style={{ width: 150, height: 20 }} active />}
      </Breadcrumb.Item>
      <Breadcrumb.Separator>
        <Divider
          style={{
            marginLeft: 10,
            marginRight: 10,
            height: 20,
            borderLeft: '2px solid rgba(0, 0, 0, 0.06)',
          }}
          type="vertical"
        />
      </Breadcrumb.Separator>
      <Breadcrumb.Item>
        <DatabaseOutlined style={{ width: 20 }} />
        <Text style={{ fontSize: 16, whiteSpace: 'normal' }}>
          {
            datasource.datasource_name
            || <Skeleton.Input style={{ width: 100, height: 16 }} active />
          }
        </Text>
      </Breadcrumb.Item>
      <Breadcrumb.Separator />
      <Breadcrumb.Item>
        <AppstoreOutlined style={{ width: 18 }} />
        <Text style={{ fontSize: 16, whiteSpace: 'normal' }}>
          {
            (
              datasource.database && datasetSchema)
              ? `${datasource.database}.${datasetSchema}`
              : <Skeleton.Input style={{ width: 100, height: 16 }} active />
          }
        </Text>
      </Breadcrumb.Item>
      <Breadcrumb.Separator />
      <Breadcrumb.Item>
        <TableOutlined
          style={{
            width: 18,
            color: isVirtual ? '#1890FF' : 'rgba(0,0,0,.85)',
          }}
        />
        <Text style={{ fontSize: 16, whiteSpace: 'normal' }}>
          {datasetName || <Skeleton.Input style={{ width: 100, height: 16 }} active />}
        </Text>
      </Breadcrumb.Item>
    </Breadcrumb>
  );

  return (
    <div>
      <Content className="site-layout-background card-list">
        <Section style={{ margin: '24px 16px' }}>
          <PageHeader
            className="site-page-header-responsive section"
            breadcrumbRender={() => breadcrumbs}
            title={datasetName || <Skeleton.Input style={{ width: 100, height: 16 }} active />}
            extra={[
              <Tooltip key="1" placement="bottomRight" title="Copy link to dataset.">
                <Button
                  icon={<CopyOutlined />}
                  onClick={() => {
                    navigator.clipboard.writeText(window.location.href);
                    message.success('Copied to clipboard');
                  }}
                />
              </Tooltip>,
            ]}
            footer={(
              <Tabs
                size="large"
                activeKey={activeTab}
                defaultActiveKey="1"
                tabBarExtraContent={tabBarActions}
                onChange={(tabKey) => setActiveTab(tabKey)}
              >
                <TabPane tab="Expectations" key="1">
                  <Row
                    align="space-between"
                    style={{ alignItems: 'center' }}
                  >
                    <ExpectationModal
                      visible={expectationModal.visible}
                      type={expectationModal.type}
                      editedExpectation={expectationModal.expectation}
                      dataset={expectationModal.dataset}
                      onCancel={() => {
                        setExpectationModal({
                          visible: false, type: '', expectation: null, dataset: null,
                        });
                      }}
                      onFormSubmit={() => {
                        setExpectationModal({
                          visible: false, type: '', expectation: null, dataset: null,
                        });
                        setRefreshExpectations(true);
                      }}
                    />
                  </Row>
                  <Table
                    columns={columns}
                    dataSource={expectationsList}
                    loading={requestInProgress}
                    pagination={{ position: ['bottomRight'] }}
                    rowKey={() => uuidv4()}
                  />
                </TabPane>
                <TabPane tab="Sample" key="2">
                  <DataSample
                    columns={dataset.sample?.columns ? dataset.sample?.columns : []}
                    rows={dataset.sample?.rows ? dataset.sample?.rows : []}
                  />
                </TabPane>
                {
                  dataset?.runtime_parameters?.query
                    ? (
                      <TabPane tab="Query" key="3">
                        <Col style={{ marginTop: 24, marginBottom: 24 }}>
                          {
                            dataset?.runtime_parameters?.query
                              ? (
                                <CodeEditor
                                  readOnly
                                  value={dataset.runtime_parameters.query}
                                />
                              )
                              : (
                                <div className="ant-skeleton ant-skeleton-element ant-skeleton-active" style={{ width: '100%' }}>
                                  <span className="ant-skeleton-input" style={{ height: '100px' }} />
                                </div>
                              )
                          }
                        </Col>
                      </TabPane>
                    )
                    : null
                }
                <TabPane tab="Suggestions" key="4">
                  <Table
                    columns={suggestionsColumns}
                    dataSource={suggestionsList}
                    loading={requestInProgress}
                    pagination={{ position: ['bottomRight'] }}
                    rowKey={() => uuidv4()}
                  />
                </TabPane>
                <TabPane tab="Schedules" key="5">
                  <Row
                    align="space-between"
                    style={{ alignItems: 'center' }}
                  >
                    <ScheduleModal
                      visible={scheduleModal.visible}
                      type={scheduleModal.type}
                      editedSchedule={scheduleModal.schedule}
                      trigger={scheduleModal.trigger}
                      datasetId={datasetId}
                      onCancel={() => {
                        setScheduleModal({
                          visible: false, type: '', schedule: null, trigger: '',
                        });
                      }}
                      onFormSubmit={() => {
                        setScheduleModal({
                          visible: false, type: '', schedule: null, trigger: '',
                        });
                        setRefreshSchedules(true);
                      }}
                    />
                  </Row>
                  <Table
                    columns={scheduleColumns}
                    dataSource={schedules}
                    loading={requestInProgress}
                    pagination={{ position: ['bottomRight'] }}
                    rowKey={() => uuidv4()}
                  />
                </TabPane>
              </Tabs>
            )}
          >
            <Content>
              {datasetMetaData()}
              <Divider style={{ margin: '12px 0' }} />
              <SLAHitRate stats={validationStats} />
            </Content>
          </PageHeader>
        </Section>
      </Content>
    </div>
  );
});

export default Dataset;
