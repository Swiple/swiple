import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Col, Form, Input, message, Row, Select, Space,
} from 'antd';
import { CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import Text from 'antd/es/typography/Text';
import Modal from './Modal';
import {
  getActionsJsonSchema, getDestinations, getUsers, postAction, putAction,
} from '../Api';
import AsyncButton from './AsyncButton';
import { capitalizeFirstLetter, getDestinationIcon } from '../Utils';

const { Option } = Select;
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

function ActionModal({
  visible,
  type,
  editedResource,
  resourceKey,
  resourceType,
  actionTypeOptions,
  onCancel,
  onFormSubmit,
}) {
  const [refreshJsonSchema, setRefreshJsonSchema] = useState(true);
  const [jsonSchema, setJsonSchema] = useState([]);
  const [refreshDestinations, setRefreshDestinations] = useState(true);
  const [destinations, setDestinations] = useState([]);
  const [users, setUsers] = useState([]);
  const [refreshUsers, setRefreshUsers] = useState(true);
  const [selectedDestination, setSelectedDestination] = useState('');
  const [responseStatus, setResponseStatus] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    if (refreshDestinations) {
      getDestinations()
        .then((response) => {
          if (response.status === 200) {
            setDestinations(response.data);
            setRefreshDestinations(false);
          } else {
            message.error('An error occurred while retrieving destinations.', 5);
          }
        });
    }
  }, [refreshJsonSchema, setRefreshJsonSchema]);

  useEffect(() => {
    if (refreshJsonSchema) {
      getActionsJsonSchema()
        .then((response) => {
          if (response.status === 200) {
            setJsonSchema(response.data);
            setRefreshJsonSchema(false);
          } else {
            message.error('An error occurred while retrieving actions schema.', 5);
          }
        });
    }
  }, [refreshJsonSchema, setRefreshJsonSchema]);

  useEffect(() => {
    if (refreshUsers) {
      getUsers()
        .then((response) => {
          if (response.status === 200) {
            setUsers(response.data);
          } else {
            message.error('An error occurred while retrieving users.', 5);
          }
          setRefreshUsers(false);
        });
    }
  }, [refreshUsers, setRefreshUsers]);

  useEffect(() => {
    if (type === UPDATE_TYPE && editedResource !== null) {
      form.setFieldsValue(editedResource);
      setSelectedDestination(editedResource?.destination?.destination_name);
    }
  }, [type, UPDATE_TYPE, editedResource]);

  const createOrUpdateResourceRequest = async (payload) => {
    if (type === CREATE_TYPE) {
      return postAction(payload).then((response) => response);
    }
    return putAction(payload, editedResource.key).then((response) => response);
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch(() => ({ complete: false, values: {} }));

  const transformPayload = (payload) => {
    const transformedPayload = payload;
    transformedPayload.destination.kwargs.destination_type = destinations.filter(
      (item) => item.destination_name === selectedDestination,
    )[0].kwargs.destination_type;

    transformedPayload.destination.destination_name = selectedDestination;
    delete transformedPayload.destination_name;
    transformedPayload.resource_key = resourceKey;
    transformedPayload.resource_type = resourceType;

    return transformedPayload;
  };

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const transformedDatasetPayload = transformPayload(values);
      const { status, data } = await createOrUpdateResourceRequest(transformedDatasetPayload);

      if (status === 200 || status === 201) {
        setResponseStatus({ success: true });

        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          form.resetFields();
          setSelectedDestination('');
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

  const destinationOptions = () => destinations.map((item) => (
    <Option
      key={item.key}
      value={item.destination_name}
      label={item.destination_name}
    >
      <Row align="start" style={{ alignItems: 'center', color: 'black' }}>
        <Space>
          <div className="select-option">
            <img
              style={{ position: 'relative' }}
              src={getDestinationIcon(item.kwargs.destination_type)}
              alt={`${item.kwargs.destination} icon`}
              width="20"
              height="20"
            />
          </div>
          {item.destination_name}
        </Space>
      </Row>
    </Option>
  ));

  const getResponseStatus = () => {
    if (responseStatus === null) {
      return null;
    }
    if (responseStatus.success) {
      return (
        <Space>
          <CheckCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#52c41a" />
          <Text style={{ fontSize: 16, whiteSpace: 'normal' }} type="success">
            Action looks good!
          </Text>
        </Space>
      );
    }
    if (!responseStatus.success) {
      return (
        <Space>
          <CloseCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#FF4D4F" />
          <Text style={{ fontSize: 16, color: '#FF4D4F', whiteSpace: 'normal' }}>
            {responseStatus.msg}
          </Text>
        </Space>
      );
    }
    return null;
  };

  const onCancelInternal = () => {
    // parent event callback
    onCancel();
    form.resetFields();
    setSelectedDestination('');
  };

  const userOptions = () => users.map((item) => (
    <Option
      key={item.email}
      value={item.email}
      label={item.email}
    >
      <Row align="start" style={{ alignItems: 'center', color: 'black' }}>
        {item.email}
      </Row>
    </Option>
  ));

  const formInputType = (propObj, placeholder) => {
    if (propObj?.enum) {
      return (
        <Select>
          {
            propObj.enum.map((item) => <Option key={item} value={item}>{item}</Option>)
          }
        </Select>
      );
    }

    if (propObj.type === 'array' && propObj?.items.format === 'email') {
      return (
        <Select mode="tags" allowClear>
          {userOptions()}
        </Select>
      );
    }
    return (
      <Input placeholder={placeholder} />
    );
  };

  const buildForm = () => {
    // Don't show these form items in the generated form
    const ignoredFormItem = ['key', 'create_date', 'created_by', 'modified_date', 'destination_name', 'destination_type'];

    if (selectedDestination !== '') {
      const destinationType = destinations.filter(
        (item) => item.destination_name === selectedDestination,
      )[0].kwargs.destination_type;
      return jsonSchema.map((formItemObj) => {
        if (destinationType === formItemObj.title) {
          return Object.keys(formItemObj.properties).map((formItem) => {
            if (!ignoredFormItem.includes(formItem)) {
              const propObj = formItemObj.properties[formItem];
              const placeholder = propObj.placeholder ? propObj.placeholder : null;
              return (
                <Form.Item
                  key={propObj.title}
                  label={propObj.title}
                  name={['destination', 'kwargs', formItem]}
                  tooltip={propObj.description ? propObj.description : null}
                  rules={[
                    formItemObj.required.includes(formItem)
                      ? { required: true, message: 'required field.' }
                      : {},
                  ]}
                >
                  {formInputType(propObj, placeholder)}
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

  const getActionTypeOptions = () => actionTypeOptions.map((item) => (
    <Option
      key={item.actionType}
      value={item.actionType}
      label={item.actionType}
      className="select-option-border-bottom"
    >
      <Col className="select-with-text-wrap" align="start" style={{ alignItems: 'center', color: 'black' }}>
        <div>
          <Text strong style={{ fontSize: 16 }}>
            {capitalizeFirstLetter(item.actionType)}
          </Text>
        </div>
        <div style={{ marginTop: 10 }} />
        <div>{item.description}</div>
      </Col>
    </Option>
  ));

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Action' : 'Update Action'}
      visible={visible}
      onCancel={() => {
        onCancelInternal();
        return onCancel();
      }}
      width={600}
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
          label="Action Type"
          name="action_type"
          rules={[
            {
              required: true,
              message: 'Select an action type',
            },
          ]}
        >
          <Select>
            {getActionTypeOptions()}
          </Select>
        </Form.Item>
        <Form.Item
          label="Destination"
          name={['destination', 'destination_name']}
          rules={[
            {
              required: true,
              message: 'Select a destination',
            },
          ]}
        >
          <Select
            onChange={(value) => {
              setSelectedDestination(value);
            }}
          >
            {destinationOptions()}
          </Select>
        </Form.Item>
        {buildForm()}
        <Row style={{ minHeight: 25 }} justify="start" align="top">
          {getResponseStatus()}
        </Row>
      </Form>
    </Modal>
  );
}

ActionModal.defaultProps = {
  visible: false,
  editedResource: {},
};

ActionModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  resourceKey: PropTypes.string.isRequired,
  resourceType: PropTypes.string.isRequired,
  actionTypeOptions: PropTypes.arrayOf(PropTypes.shape({
    actionType: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
  })).isRequired,
  editedResource: PropTypes.objectOf(Object),
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default ActionModal;
