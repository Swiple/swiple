import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Form, Input, message, Modal, Row, Select, Space, Typography,
} from 'antd';
import { CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import {
  AthenaIcon, BigqueryIcon, MysqlIcon, PostgresqlIcon, RedshiftIcon, SnowflakeIcon,
} from '../../../static/images';
import { getDataSourcesJsonSchema, postDataSource, putDataSource } from '../../../Api';
import AsyncButton from '../../../components/AsyncButton';

const Ajv = require('ajv');

const ajv = new Ajv();
ajv.addKeyword('placeholder');

const { Option } = Select;
const { Text } = Typography;
const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function DatasourceModal({
  visible, type, editedDatasource, engine, onCancel, onFormSubmit,
}) {
  const [refreshDataSourcesJsonSchema, setRefreshDataSourcesJsonSchema] = useState(true);
  const [dataSourcesJsonSchema, setDataSourcesJsonSchema] = useState([]);
  const [selectedEngine, setSelectedEngine] = useState('');
  const [responseStatus, setResponseStatus] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    if (type === UPDATE_TYPE && editedDatasource !== null) {
      form.setFieldsValue(editedDatasource);
      setSelectedEngine(engine);
    }
  }, [type, UPDATE_TYPE, editedDatasource]);

  useEffect(() => {
    if (refreshDataSourcesJsonSchema) {
      getDataSourcesJsonSchema()
        .then((response) => {
          if (response.status === 200) {
            setDataSourcesJsonSchema(response.data);
            setRefreshDataSourcesJsonSchema(false);
          } else {
            message.error('An error occurred while retrieving data sources schema.', 5);
          }
        });
    }
  }, [refreshDataSourcesJsonSchema, setRefreshDataSourcesJsonSchema]);

  const createOrUpdateDatasourceRequest = async (payload) => {
    if (type === CREATE_TYPE) {
      return postDataSource(payload).then((response) => response);
    }
    return putDataSource(payload, editedDatasource.key).then((response) => response);
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch((validationInfo) => {
      console.log('Validations failed: ', validationInfo);
      return { complete: false, values: {} };
    });

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const { status, data } = await createOrUpdateDatasourceRequest(values);

      if (status === 200) {
        setResponseStatus({ success: true });

        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          setSelectedEngine('');
          form.resetFields();
        }, 500);
      } else if (status === undefined) {
        message.error('API appears to be down.', 5);
      } else if (data?.detail !== undefined) {
        setResponseStatus({ success: false, msg: data.detail });
      } else {
        message.error('An unknown error occurred.', 5);
      }
    } else {
      setResponseStatus(null);
    }
    return null;
  };

  const handleNumberInput = (value, prop) => {
    const obj = {};
    if (value !== '') {
      obj[prop] = parseInt(value, 10);
      form.setFieldsValue(obj);
    }
  };

  const buildValidationErrors = (errorList) => {
    let errorString = '';
    for (let i = 0; i < errorList.length; i += 1) {
      const { msg } = errorList[i];
      if (msg && !msg.includes('unknown keyword')) {
        errorString += `${msg}\n`;
      }
    }
    return errorString;
  };

  /**
   * Uses OpenAPI datasource model schema to dynamically build a form.
   */
  const buildDataSourceForm = () => {
    // Don't show these form items in the generated form
    const ignoredFormItem = ['key', 'create_date', 'created_by', 'modified_date', 'datasource_name', 'engine', 'description'];

    if (selectedEngine !== '') {
      return dataSourcesJsonSchema.map((formItemObj) => {
        if (selectedEngine === formItemObj.title) {
          return Object.keys(formItemObj.properties).map((formItem) => {
            if (!ignoredFormItem.includes(formItem)) {
              const propObj = formItemObj.properties[formItem];
              const placeholder = propObj.placeholder ? propObj.placeholder : null;
              return (
                <Form.Item
                  key={propObj.title}
                  label={propObj.title}
                  name={formItem}
                  tooltip={propObj.description ? propObj.description : null}
                  rules={[
                    formItemObj.required.includes(formItem)
                      ? { required: true, message: 'required field.' }
                      : null,
                    {
                      validator: async (rule, value) => {
                        const validate = ajv.compile(propObj);
                        const valid = validate(value);
                        // no need to validate undefined values as we have 'required' rule above
                        if (value !== undefined && !valid) {
                          throw new Error(buildValidationErrors(validate.errors));
                        }
                      },
                    },
                  ]}
                >
                  {
                    propObj.type === 'integer'
                      ? (
                        <Input
                          placeholder={placeholder}
                          onChange={(e) => handleNumberInput(e.target.value, formItem)}
                        />
                      )
                      : <Input placeholder={placeholder} />
                  }
                </Form.Item>
              );
            }
            return null;
          });
        }
        return null;
      });
    }
    return null;
  };

  const getEngineOptions = () => {
    const datasourceImgMap = {
      postgresql: PostgresqlIcon,
      redshift: RedshiftIcon,
      snowflake: SnowflakeIcon,
      mysql: MysqlIcon,
      bigquery: BigqueryIcon,
      athena: AthenaIcon,
    };

    return dataSourcesJsonSchema.map((item) => {
      const imgPath = datasourceImgMap[item.title.toLowerCase()];
      return (
        <Option
          key={item.title}
          value={item.title}
          label={item.title}
        >
          <Row align="start" style={{ alignItems: 'center', color: 'black' }}>
            <Space>
              <div className="select-option">
                <img
                  style={{ position: 'relative' }}
                  src={imgPath}
                  alt={item.title}
                  width="20"
                  height="20"
                />
              </div>
              {item.title}
            </Space>
          </Row>
        </Option>
      );
    });
  };

  const getResponseStatus = () => {
    if (responseStatus === null) {
      return null;
    }
    if (responseStatus.success) {
      return (
        <Space>
          <CheckCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#52c41a" />
          <Text style={{ fontSize: 16, whiteSpace: 'normal' }} type="success">Connection looks good!</Text>
        </Space>
      );
    }
    if (!responseStatus.success) {
      return (
        <Space>
          <CloseCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#FF4D4F" />
          <Text style={{ fontSize: 16, color: '#FF4D4F', whiteSpace: 'normal' }}>{responseStatus.msg}</Text>
        </Space>
      );
    }
    return null;
  };

  const onCancelInternal = () => {
    // parent event callback
    onCancel();
    setResponseStatus(null);
    form.resetFields();
    setSelectedEngine('');
  };

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Datasource' : 'Update Datasource'}
      visible={visible}
      onCancel={() => {
        onCancelInternal();
        return onCancel();
      }}
      width={600}
      bodyStyle={{
        maxHeight: '900px',
        overflowWrap: 'break-word',
        overflow: 'auto',
      }}
      wrapClassName="wrapper-class"
      footer={[
        <Button
          key="cancel"
          onClick={() => {
            onCancelInternal();
            return onCancel();
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
        {...layout}
        name="dynamic_form_nest_item"
        form={form}
        layout="vertical"
        size="large"
        preserve={false}
      >
        <Form.Item
          label="Data Source Name"
          name="datasource_name"
          rules={[
            {
              required: true,
              message: 'Enter a data source name',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Description"
          name="description"
          rules={[
            {
              required: true,
              message: 'Enter a description',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="engine"
          label="Engine"
          rules={[{ required: true, message: 'Select an engine.' }]}
        >
          <Select
            onChange={(value) => setSelectedEngine(value)}
          >
            {getEngineOptions()}
          </Select>
        </Form.Item>
        {buildDataSourceForm()}
        <Row style={{ minHeight: 25 }} justify="start" align="top">
          {getResponseStatus()}
        </Row>
      </Form>
    </Modal>
  );
}

DatasourceModal.defaultProps = {
  visible: false,
  editedDatasource: {},
  engine: '',
};

DatasourceModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedDatasource: PropTypes.objectOf(Object),
  engine: PropTypes.string,
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default DatasourceModal;
