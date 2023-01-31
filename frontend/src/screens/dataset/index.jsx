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
  getExpectations,
  getValidationStats,
  postRunnerValidateDataset,
  putSample,
  getSchedulesForDataset,
  deleteSchedule,
  suggestExpectations,
  enableExpectation,
  deleteAction,
  getActions,
} from '../../Api';
import Section from '../../components/Section';
import CodeEditor from './components/CodeEditor';
import ExpectationHistory from './components/ExpectationHistory';
import ObjectiveHitRate from './components/ObjectiveHitRate';
import DataSample from './components/DataSample';
import AsyncButton from '../../components/AsyncButton';
import ExpectationModal, { CREATE_TYPE, UPDATE_TYPE } from './components/ExpectationModal';
import ScheduleModal from './components/ScheduleModal';
import { splitDatasetResource, getEngineIcon, getDestinationIcon } from '../../Utils';
import ActionModal from '../../components/ActionModal';

const { Content } = Layout;
const { Text } = Typography;
const { TabPane } = Tabs;
const { confirm } = Modal;

// Tab Names
const EXPECTATIONS = 'expectations';
const SAMPLE = 'sample';
const QUERY = 'query';
const SUGGESTIONS = 'suggestions';
const SCHEDULES = 'schedules';
const ACTIONS = 'actions';

const ACTION_TYPE_OPTIONS = [
  { actionType: 'validation', description: 'Triggered when data validation completes.' },
];

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
  const [expectationModal, setExpectationModal] = useState({ visible: false, type: '', dataset: null });
  const [scheduleModal, setScheduleModal] = useState({ visible: false, type: '', editedSchedule: null });
  const [actionModal, setActionModal] = useState({ visible: false, type: '', editedResource: null });
  const [refreshActions, setRefreshActions] = useState(true);
  const [actions, setActions] = useState([]);

  const history = useHistory();
  const query = useQuery();
  const datasetId = query.get('dataset-id');
  const tab = query.get('tab');

  const [activeTab, setActiveTab] = useState(tab || EXPECTATIONS);

  const { datasetSchema, datasetName, isVirtual } = splitDatasetResource(dataset);

  useEffect(() => {
    if (!tab) {
      history.replace({
        pathname: '/dataset/home',
        search: `?dataset-id=${datasetId}&tab=${activeTab}`,
      });
    }
  }, [activeTab]);

  useEffect(() => {
    if (refreshActions) {
      getActions(datasetId)
        .then((response) => {
          if (response.status === 200) {
            setActions(response.data);
          } else {
            message.error('An error occurred while retrieving actions.', 5);
          }
          setRefreshActions(false);
        });
    }
  }, [refreshActions, setRefreshActions]);

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
      getExpectations(datasetId, null, true, null, true)
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
      getExpectations(datasetId, null, false, true, false)
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
        setDataset({
          ...dataset,
          sample: putSampleResponse.data.sample,
        });
        resolve();
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

  const openActionModal = (modalType, record = null) => {
    let action;
    if (modalType === UPDATE_TYPE) {
      [action] = actions.filter((item) => item.key === record.key);
    }
    setActionModal({
      visible: true,
      type: modalType,
      editedResource: action,
    });
  };

  const rejectSuggestion = (record) => new Promise((resolve) => {
    deleteExpectation(record.key).then(() => {
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
                enableExpectation(record.key).then((response) => {
                  if (response.status === 200) {
                    setSuggestions(suggestions.filter((item) => item.key !== record.key));
                    setRefreshExpectations(true);
                    resolve();
                  } else if (response.status === 422) {
                    message.warn(response.data.detail, 10);
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

  const removeAction = (record) => new Promise((resolve, reject) => {
    deleteAction(record.key).then(() => {
      setRefreshValidationStats(true);
      setActions(actions.filter((item) => item.key !== record.key));
      resolve();
    }).catch(() => reject());
  });

  const showActionDeleteModal = (record) => {
    confirm({
      title: 'Delete Action',
      icon: <ExclamationCircleOutlined />,
      content: "Are you sure you'd like to delete this action?",
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeAction(record);
      },
      onCancel() {},
    });
  };

  const destinationMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openActionModal(UPDATE_TYPE, record)}
      >
        Edit
      </Menu.Item>
      <Menu.Item
        key="2"
        onClick={() => showActionDeleteModal(record)}
        icon={<DeleteFilled style={{ color: 'red' }} />}
      >
        Delete
      </Menu.Item>
    </Menu>
  );

  const columns = [
    {
      title: 'COLUMN',
      dataIndex: 'column',
      width: 200,
      render: (text) => (
        <div style={{ wordWrap: 'break-word', wordBreak: 'break-word' }}>
          {text}
        </div>
      ),
    },
    {
      title: 'EXPECTATION',
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
        if (activeTab === EXPECTATIONS) {
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
      title: 'NEXT RUN TIME',
      dataIndex: 'next_run_time',
      render: (text) => (
        moment(text).local().format('ddd, D MMM YYYY HH:mm:ss Z')
      ),
    },
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

  const actionsColumns = [
    {
      title: 'ACTION_TYPE',
      dataIndex: 'action_type',
    },
    {
      title: 'DESTINATION NAME',
      dataIndex: ['destination', 'destination_name'],
    },
    {
      title: 'DESTINATION TYPE',
      dataIndex: ['destination', 'kwargs', 'destination_type'],
      render: (text) => (
        <img
          style={{
            position: 'relative',
            width: 20,
            height: 20,
            marginRight: 8,
          }}
          src={getDestinationIcon(text)}
          alt={text}
        />
      ),
    },
    {
      title: 'LAST MODIFIED',
      dataIndex: 'modified_date',
      render: (text) => moment(text).local().fromNow(),
    },
    {
      title: '',
      render: (text, record) => (
        <Dropdown
          trigger={['click']}
          overlay={destinationMenu(record)}
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

  const expectationsList = expectations.map((item) => ({
    key: item.key,
    expectation_type: item.expectation_type,
    validations: item.validations,
    documentation: item.documentation,
    column: item.kwargs?.column ? item.kwargs.column : '',
    kwargs: item.kwargs,
    resultType: item.result_type,
    create_date: moment(item.create_date).local().fromNow(),
    modified_date: moment(item.modified_date).local().fromNow(),
  }));

  const analyzeDataset = () => new Promise((resolve) => {
    postRunnerValidateDataset(datasetId).then(() => {
      setRefreshValidationStats(true);
      setRefreshExpectations(true);
      resolve();
    });
  });

  const suggestExpectationsForDataset = () => new Promise((resolve) => {
    setSuggestions([]);
    suggestExpectations(datasetId).then(() => {
      setRefreshSuggestions(true);
      resolve();
    });
  });

  const tabBarActions = (
    <Space>
      {
        activeTab === EXPECTATIONS
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
        activeTab === SAMPLE
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
        activeTab === SUGGESTIONS
          ? (
            <AsyncButton
              style={{ fontWeight: 'bold' }}
              type="primary"
              size="medium"
              onClick={() => suggestExpectationsForDataset()}
            >
              Generate Suggestions
            </AsyncButton>
          )
          : null
      }
      {
        activeTab === SCHEDULES
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
      {
        activeTab === ACTIONS
          ? (
            <Button
              className="card-list-button-dark"
              style={{ fontWeight: 'bold' }}
              type="primary"
              icon={<PlusOutlined />}
              size="medium"
              onClick={() => openActionModal(CREATE_TYPE)}
            >
              Action
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
                defaultActiveKey={activeTab}
                tabBarExtraContent={tabBarActions}
                onChange={(tabKey) => {
                  setActiveTab(tabKey);
                  history.replace({
                    pathname: '/dataset/home',
                    search: `?dataset-id=${datasetId}&tab=${tabKey}`,
                  });
                }}
              >
                <TabPane tab="Expectations" key={EXPECTATIONS}>
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
                <TabPane tab="Sample" key={SAMPLE}>
                  <DataSample
                    columns={dataset.sample?.columns ? dataset.sample?.columns : []}
                    rows={dataset.sample?.rows ? dataset.sample?.rows : []}
                  />
                </TabPane>
                {
                  dataset?.runtime_parameters?.query
                    ? (
                      <TabPane tab="Query" key={QUERY}>
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
                <TabPane tab="Suggestions" key={SUGGESTIONS}>
                  <Table
                    columns={suggestionsColumns}
                    dataSource={suggestionsList}
                    loading={requestInProgress}
                    pagination={{ position: ['bottomRight'] }}
                    rowKey={() => uuidv4()}
                  />
                </TabPane>
                <TabPane tab="Schedules" key={SCHEDULES}>
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
                <TabPane tab="Actions" key={ACTIONS}>
                  <Row
                    align="space-between"
                    style={{ alignItems: 'center' }}
                  >
                    <ActionModal
                      visible={actionModal.visible}
                      type={actionModal.type}
                      resourceKey={datasetId}
                      resourceType="dataset"
                      actionTypeOptions={ACTION_TYPE_OPTIONS}
                      editedResource={actionModal.editedResource}
                      onCancel={() => {
                        setActionModal({
                          visible: false, type: '',
                        });
                      }}
                      onFormSubmit={() => {
                        setActionModal({
                          visible: false, type: '',
                        });
                        setRefreshActions(true);
                      }}
                    />
                  </Row>
                  <Table
                    columns={actionsColumns}
                    dataSource={actions}
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
              <ObjectiveHitRate stats={validationStats} />
            </Content>
          </PageHeader>
        </Section>
      </Content>
    </div>
  );
});

export default Dataset;
