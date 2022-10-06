import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Form, Input, message, Row, Select, Space,
} from 'antd';
import {
  CheckCircleTwoTone,
  CloseCircleTwoTone,
  EyeInvisibleOutlined,
  EyeTwoTone,
  LockOutlined,
} from '@ant-design/icons';
import Text from 'antd/es/typography/Text';
import Modal from '../../../components/Modal';
import {
  getDestinationsJsonSchema, postDestination, putDestination,
} from '../../../Api';
import AsyncButton from '../../../components/AsyncButton';

import ajv from '../../../JsonSchemaFormValidator';
import { getDestinationIcon } from '../../../Utils';

const { Option } = Select;

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function DestinationModal({
  visible, type, editedDestination, onCancel, onFormSubmit,
}) {
  const [refreshDestinationJsonSchema, setRefreshDestinationJsonSchema] = useState(true);
  const [destinationJsonSchema, setDestinationJsonSchema] = useState([]);
  const [selectedDestination, setSelectedDestination] = useState('');
  const [responseStatus, setResponseStatus] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    if (refreshDestinationJsonSchema) {
      getDestinationsJsonSchema()
        .then((response) => {
          if (response.status === 200) {
            setDestinationJsonSchema(response.data);
            setRefreshDestinationJsonSchema(false);
          } else {
            message.error('An error occurred while retrieving destination schema.', 5);
          }
        });
    }
  }, [refreshDestinationJsonSchema, setRefreshDestinationJsonSchema]);

  useEffect(() => {
    if (type === UPDATE_TYPE && editedDestination !== null) {
      form.setFieldsValue(editedDestination);
      setSelectedDestination(editedDestination.kwargs.destination_type);
    }
  }, [type, UPDATE_TYPE, editedDestination]);

  const createOrUpdateDestinationRequest = async (payload) => {
    if (type === CREATE_TYPE) {
      return postDestination(payload).then((response) => response);
    }
    return putDestination(payload, editedDestination.key).then((response) => response);
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch(() => ({ complete: false, values: {} }));

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const { status, data } = await createOrUpdateDestinationRequest(values);

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

  const destinationOptions = () => destinationJsonSchema.map((item) => (
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
              src={getDestinationIcon(item.title)}
              alt={`${item.title} icon`}
              width="20"
              height="20"
            />
          </div>
          {item.title}
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
            Destination looks good!
          </Text>
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
    form.resetFields();
    setSelectedDestination('');
  };

  const buildValidationErrors = (errorList) => {
    let errorString = '';
    for (let i = 0; i < errorList.length; i += 1) {
      const { message } = errorList[i];
      if (message && !message.includes('unknown keyword')) {
        errorString += `${message}\n`;
      }
    }
    return errorString;
  };

  const usePasswordIconRender = (isVisible) => {
    if (type !== CREATE_TYPE) return null;
    return isVisible ? <EyeTwoTone /> : <EyeInvisibleOutlined />;
  };

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

    if (propObj.format === 'password') {
      return (
        <Input.Password
          placeholder={placeholder}
          type="password"
          prefix={<LockOutlined />}
          iconRender={(isVisible) => usePasswordIconRender(isVisible)}
        />
      );
    }

    return (
      <Input
        placeholder={placeholder}
        type="text"
      />
    );
  };

  const buildForm = () => {
    // Don't show these form items in the generated form
    const ignoredFormItem = ['key', 'create_date', 'created_by', 'modified_date', 'destination_name', 'destination_type'];
    if (selectedDestination !== '') {
      return destinationJsonSchema.map((formItemObj) => {
        if (selectedDestination === formItemObj.title) {
          return Object.keys(formItemObj.properties).map((formItem) => {
            if (!ignoredFormItem.includes(formItem)) {
              const propObj = formItemObj.properties[formItem];
              const placeholder = propObj.placeholder ? propObj.placeholder : null;
              return (
                <Form.Item
                  key={propObj.title}
                  label={propObj.title}
                  name={['kwargs', formItem]}
                  tooltip={propObj.description ? propObj.description : null}
                  rules={[
                    formItemObj.required.includes(formItem)
                      ? { required: true, message: 'required field.' }
                      : {},
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

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Destination' : 'Update Destination'}
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
        name="dynamic_form_nest_item"
        form={form}
        layout="vertical"
        size="large"
        preserve={false}
      >
        <Form.Item
          label="Destination Name"
          name="destination_name"
          rules={[
            {
              required: true,
              message: 'Enter a destination name',
            },
          ]}
        >
          <Input spellcheck="false" />
        </Form.Item>
        <Form.Item
          label="Destination Type"
          name={['kwargs', 'destination_type']}
          rules={[
            {
              required: true,
              message: 'Select the destination type',
            },
          ]}
        >
          <Select
            disabled={type === UPDATE_TYPE}
            onChange={(value) => {
              // Remove any existing destination kwargs when destination_type is changed
              form.setFieldsValue({
                destination_name: form.getFieldValue('destination_name'),
                kwargs: {
                  destination_type: form.getFieldValue(['kwargs', 'destination_type']),
                },
              });
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

DestinationModal.defaultProps = {
  visible: false,
  editedDestination: {},
};

DestinationModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedDestination: PropTypes.objectOf(Object),
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default DestinationModal;
