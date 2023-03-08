import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Form, Input, Tag, message, Radio, Row, Select, Space, Typography,
} from 'antd';
import Editor from '@uiw/react-textarea-code-editor';
import { CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import Modal from '../../../components/Modal';
import AsyncButton from '../../../components/AsyncButton';
import { getEngineIcon } from '../../../Utils';
import {
  getDataSources, getSchemas, getTables, getQuerySample, postDataset, putDataset,
} from '../../../Api';
import DataSample from '../../dataset/components/DataSample';

const { Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function DatasetModal({
  visible, type, editedDataset, onCancel, onFormSubmit,
}) {
  const [dataSources, setDataSources] = useState([]);
  const [schemas, setSchemas] = useState([]);
  const [tables, setTables] = useState([]);

  const [refreshDataSources, setRefreshDataSources] = useState(true);
  const [refreshSchemas, setRefreshSchemas] = useState(false);
  const [refreshTables, setRefreshTables] = useState(false);
  const [dataSampleInProgress, setDataSampleInProgress] = useState(false);
  const [dataSample, setDataSample] = useState({});
  const [responseStatus, setResponseStatus] = useState(null);
  const [datasetType, setDatasetType] = useState('table');

  const [form] = Form.useForm();

  const handleHiddenItems = () => {
    const obj = {};
    if (!form.getFieldValue('schema')) {
      obj.query = false;
    } else if (form.getFieldValue('schema')) {
      obj.query = true;
    }
  };

  useEffect(() => {
    if (type === UPDATE_TYPE && editedDataset !== null) {
      setRefreshSchemas(true);
      if (editedDataset?.runtime_parameters?.query) {
        setDatasetType('query');

        form.setFieldsValue({
          dataset_name: editedDataset.dataset_name,
          description: editedDataset.description,
          datasource_id: editedDataset.datasource_id,
          schema: editedDataset.runtime_parameters.schema,
          query: editedDataset.runtime_parameters.query,
        });
      } else {
        setDatasetType('table');
        const splitDataset = editedDataset.dataset_name.split('.');
        form.setFieldsValue({
          dataset_name: editedDataset.dataset_name,
          description: editedDataset.description,
          datasource_id: editedDataset.datasource_id,
          schema: splitDataset[0],
          table: splitDataset[1],
        });
      }
      setRefreshTables(true);
      handleHiddenItems();
    }
  }, [type, UPDATE_TYPE, editedDataset]);

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
  }, [refreshDataSources, setRefreshDataSources]);

  useEffect(() => {
    if (refreshSchemas) {
      const datasourceId = form.getFieldsValue().datasource_id;

      getSchemas(datasourceId)
        .then((response) => {
          if (response.status === 200) {
            setSchemas(response.data);
            setResponseStatus(null);
          } else if (response.status === 422) {
            setSchemas([]);
            setResponseStatus({ success: false, msg: response.data.detail });
          } else {
            message.error('An error occurred while introspecting schemas.', 5);
          }
          setRefreshSchemas(false);
        });
    }
  }, [form, refreshSchemas]);

  useEffect(() => {
    if (refreshTables) {
      const datasourceId = form.getFieldsValue().datasource_id;
      const { schema } = form.getFieldsValue();

      getTables(datasourceId, schema)
        .then((response) => {
          if (response.status === 200) {
            setTables(response.data);
          } else {
            message.error('An error occurred while introspecting tables.', 5);
          }
          setRefreshTables(false);
        });
    }
  }, [form, refreshTables]);

  const getAdditionalFields = (datasourceId) => {
    const datasource = dataSources.filter((item) => item.key === datasourceId)[0];
    const conditional = {};

    return {
      datasource_name: datasource.datasource_name,
      database: datasource.database,
      ...conditional,
    };
  };

  const transformDatasetPayload = (payload) => {
    let transformedPayload;

    if (datasetType === 'query') {
      transformedPayload = { runtime_parameters: {} };
      const runtimeParametersFields = ['schema', 'query'];

      Object.keys(payload).forEach((key) => {
        if (runtimeParametersFields.includes(key)) {
          transformedPayload.runtime_parameters[key] = payload[key];
        } else {
          transformedPayload[key] = payload[key];
        }
      });
    } else {
      transformedPayload = {
        dataset_name: `${payload.schema}.${payload.table}`,
        description: payload.description,
        datasource_id: payload.datasource_id,
      };
    }

    const datasourceFields = getAdditionalFields(payload.datasource_id);

    return { ...transformedPayload, ...datasourceFields };
  };

  useEffect(() => {
    if (dataSampleInProgress) {
      const payload = form.getFieldsValue(true);
      const transformedDatasetPayload = transformDatasetPayload(payload);
      getQuerySample(transformedDatasetPayload)
        .then((response) => {
          if (response.status === 200) {
            setDataSample(response.data);
            setResponseStatus(null);
          } else if (response.status === 422) {
            setDataSample({});
            setResponseStatus({ success: false, msg: response.data.detail });
          } else {
            message.error('An error occurred while getting a query sample.', 5);
          }
          setDataSampleInProgress(false);
        });
    }
  }, [form, dataSampleInProgress]);

  const datasourceOptions = () => dataSources.map((item) => {
    const imgPath = getEngineIcon(item.engine);
    return (
      <Option
        key={item.key}
        value={item.datasource_id}
        label={item.datasource_name}
      >
        <Row align="start" style={{ alignItems: 'center', color: 'black' }}>
          <Space>
            <div className="select-option">
              <img
                style={{ position: 'relative' }}
                src={imgPath}
                alt="Engine Icon"
                width="20"
                height="20"
              />
            </div>
            {item.datasource_name}
          </Space>
        </Row>
      </Option>
    );
  });

  const tableOptions = () => tables.map((item) => {
    const [tableName, tableType] = item;
    const color = tableType === 'table' ? 'default' : 'blue';
    return (
      <Option
        key={tableName}
        value={tableName}
        label={tableName}
      >
        <Row align="start" style={{ alignItems: 'center', color: 'black' }}>
          <Space>
            <div className="select-option">
              <Tag color={color}>{tableType[0].toUpperCase() + tableType.slice(1)}</Tag>
            </div>
            {tableName}
          </Space>
        </Row>
      </Option>
    );
  });

  const onDatabaseChange = () => {
    form.setFieldsValue({ schema: undefined, table: undefined });
    setRefreshSchemas(true);
  };

  const getDataSample = () => new Promise((resolve) => {
    form
      .validateFields()
      .then(() => {
        setDataSampleInProgress(true);
        resolve();
      })
      .catch((info) => {
        console.log('Validate Failed:', info);
        resolve();
      });
  });

  const getResponseStatus = () => {
    if (responseStatus === null) {
      return null;
    }
    if (responseStatus.success) {
      return (
        <Space>
          <CheckCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#52c41a" />
          <Text style={{ fontSize: 16, whiteSpace: 'normal' }} type="success">Looks good!</Text>
        </Space>
      );
    }
    if (!responseStatus.success) {
      let msg = '';
      if (responseStatus?.msg) {
        // Displays sql query error messages correctly by replacing \n string with line breaks.
        msg = responseStatus?.msg.split('\n').map((text) => (
          <span key={text}>
            {text}
            <br />
          </span>
        ));
      }
      return (
        <Space>
          <CloseCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#FF4D4F" />
          <Text style={{ fontSize: 16, color: '#FF4D4F' }}>
            {msg}
          </Text>
        </Space>
      );
    }
    return null;
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch((validationInfo) => {
      console.log('Validations failed: ', validationInfo);
      return { complete: false, values: {} };
    });

  const createOrUpdateDatasetRequest = async (payload) => {
    let datasetResponse;

    if (type === CREATE_TYPE) {
      datasetResponse = postDataset(payload).then((response) => response);
    } else {
      datasetResponse = putDataset(editedDataset.key, payload).then((response) => response);
    }
    return datasetResponse;
  };

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const transformedDatasetPayload = transformDatasetPayload(values);
      const { status, data } = await createOrUpdateDatasetRequest(transformedDatasetPayload);

      if (status === 200) {
        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          setDataSample({});
          form.resetFields();
          // setHiddenItems({});
          setSchemas([]);
        }, 500);
      } else if (status === undefined) {
        message.error('API appears to be down.', 5);
      } else if (data?.detail !== undefined) {
        setResponseStatus({ success: false, msg: data?.detail });
      } else {
        message.error('An unknown error occurred.', 5);
      }
    } else {
      setResponseStatus(null);
    }
    return null;
  };

  const onCancelInternal = () => {
    setResponseStatus(null);
    form.resetFields();
    // setHiddenItems({});
    setSchemas([]);
    setDataSample({});
  };

  if (!visible || type === null) return null;

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Dataset' : 'Update Dataset'}
      visible={visible}
      onCancel={() => {
        onCancelInternal();
        return onCancel();
      }}
      width={1000}
      footer={[
        <Button
          key="cancel"
          onClick={() => {
            onCancelInternal();
            onCancel();
          }}
        >
          Cancel
        </Button>,
        <AsyncButton
          key="submit"
          type="primary"
          onClick={() => onFormSubmitInternal()}
        >
          {type === CREATE_TYPE ? 'Create' : 'Update'}
        </AsyncButton>,
      ]}
    >
      <Form
        name="dynamic_form_nest_item"
        form={form}
        layout="vertical"
        size="large"
      >
        <Form.Item
          label="Data Source"
          name="datasource_id"
          rules={[{ required: true, message: 'Select a datasource.' }]}
          style={{ width: '50%', minWidth: '360px' }}
        >
          <Select
            showSearch
            placeholder={`Select a database (${dataSources.length})`}
            onChange={onDatabaseChange}
            filterOption={(input, option) => (
              option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0
            )}
          >
            {datasourceOptions()}
          </Select>
        </Form.Item>
        <Form.Item
          label="Schema"
          name="schema"
          hidden={!schemas.length > 0}
          rules={[{ required: true, message: 'Select a schema.' }]}
          style={{ width: '50%', minWidth: '360px' }}
        >
          <Select
            showSearch
            placeholder={`Select a schema (${schemas.length})`}
            optionLabelProp="label"
            // options={() => schemaOptions()}
            onChange={() => {
              handleHiddenItems();
              form.setFieldsValue({ table: undefined });
              setRefreshTables(true);
            }}
          >
            {schemas.map((item) => (
              <Select.Option key={item} value={item}>
                {item}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>
        {
          !schemas.length > 0 || !form.getFieldValue('schema')
            ? null
            : (
              <div className="ant-row ant-form-item" style={{ width: '50%', minWidth: '360px', rowGap: '0px' }}>
                <div className="ant-col ant-form-item-label">
                  Dataset Type
                </div>
                <div className="ant-col">
                  <Radio.Group
                    options={[
                      { label: 'Table', value: 'table' },
                      { label: 'Query', value: 'query' },
                    ]}
                    onChange={(e) => {
                      setDatasetType(e.target.value);
                      form.setFieldsValue(
                        { table: undefined, query: undefined, dataset_name: undefined },
                      );
                    }}
                    value={datasetType}
                    optionType="button"
                    buttonStyle="solid"
                    size="medium"
                  />
                </div>
              </div>

            )
        }
        {
          datasetType !== 'query' || !schemas.length > 0 || !form.getFieldValue('schema')
            ? null
            : (
              <Form.Item
                label="Dataset Name"
                name="dataset_name"
                // disabled
                rules={[
                  {
                    required: true,
                    message: 'Enter a dataset name',
                  },
                ]}
                style={{ width: '50%', minWidth: '360px' }}
              >
                <Input placeholder="Dataset name" />
              </Form.Item>
            )
        }
        <Form.Item
          label="Description"
          name="description"
          rules={[
            {
              max: 500,
            },
          ]}
          style={{ width: '50%', minWidth: '360px' }}
        >
          <TextArea
            rows={2}
            placeholder="Enter a description"
          />
        </Form.Item>
        {
          datasetType !== 'table' || !schemas.length > 0 || !form.getFieldValue('schema')
            ? null
            : (
              <>
                <Form.Item
                  label="Table"
                  name="table"
                  rules={[{ required: true, message: 'Select a table.' }]}
                  style={{ width: '50%', minWidth: '360px' }}
                >
                  <Select
                    showSearch
                    placeholder={`Select a table (${tables.length})`}
                    filterOption={(input, option) => (
                      option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0
                    )}
                  >
                    {tableOptions()}
                  </Select>
                </Form.Item>
                <Form.Item
                  shouldUpdate
                >
                  {() => (
                    <AsyncButton
                      type="primary"
                      size="medium"
                      onClick={getDataSample}
                      loading={dataSampleInProgress}
                      disabled={
                        !form.getFieldValue('table')
                      }
                      ghost
                      style={{ float: 'right' }}
                    >
                      View Sample
                    </AsyncButton>
                  )}
                </Form.Item>
              </>
            )
        }
        {
          datasetType !== 'query' || !schemas.length > 0 || !form.getFieldValue('schema')
            ? null
            : (
              <>
                <Form.Item
                  label="Query"
                  name="query"
                  rules={[{ required: true, message: 'Query required.' }]}
                >
                  <Editor
                    language="sql"
                    placeholder="Enter your SQL query."
                    padding={15}
                    style={{
                      fontFamily:
                        'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
                      fontSize: 16,
                      borderRadius: '8px',
                    }}
                  />
                </Form.Item>
                <Form.Item
                  shouldUpdate
                >
                  {() => (
                    <AsyncButton
                      type="primary"
                      size="medium"
                      onClick={getDataSample}
                      loading={dataSampleInProgress}
                      disabled={
                        !form.getFieldValue('query')
                      }
                      ghost
                      style={{ float: 'right' }}
                    >
                      Test Query
                    </AsyncButton>
                  )}
                </Form.Item>
              </>
            )
        }
        <DataSample
          columns={dataSample?.columns ? dataSample?.columns : []}
          rows={dataSample?.rows ? dataSample?.rows : []}
        />
        <Row
          align="top"
          justify="start"
          style={{ minHeight: 25 }}
        >
          {getResponseStatus()}
        </Row>
      </Form>
    </Modal>
  );
}

DatasetModal.defaultProps = {
  visible: false,
  editedDataset: {
    key: null,
    dataset_name: null,
    description: null,
    datasource_id: null,
    runtime_parameters: {
      schema: null,
      query: null,
    },
  },
};

DatasetModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedDataset: PropTypes.shape({
    key: PropTypes.string,
    dataset_name: PropTypes.string,
    description: PropTypes.string,
    datasource_id: PropTypes.string,
    runtime_parameters: PropTypes.shape({
      schema: PropTypes.string,
      query: PropTypes.string,
    }),
  }),
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default DatasetModal;
