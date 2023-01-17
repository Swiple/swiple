import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Checkbox, Form, Input, message, Row, Space,
} from 'antd';
import {
  CheckCircleTwoTone,
  CloseCircleTwoTone,
  EyeInvisibleOutlined,
  EyeTwoTone, LockOutlined,
} from '@ant-design/icons';
import Text from 'antd/es/typography/Text';
import Modal from '../../../components/Modal';
import {
  postUser, patchUser,
} from '../../../Api';
import AsyncButton from '../../../components/AsyncButton';
import { formatErrorMsg } from '../../../Utils';

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function UserModal({
  visible, type, editedUser, onCancel, onFormSubmit,
}) {
  const [responseStatus, setResponseStatus] = useState(null);
  const [form] = Form.useForm();
  const [passwordValidationRequirements, setPasswordValidationRequirements] = useState({
    length: undefined,
    upperCase: undefined,
    number: undefined,
    specialChar: undefined,
  });
  const [validationStatus, setValidationStatus] = useState('success');

  useEffect(() => {
    if (type === UPDATE_TYPE && editedUser !== null) {
      const user = {
        email: editedUser.email,
        is_superuser: editedUser.is_superuser,
        is_active: editedUser.is_active,
        is_verified: true,
      };
      form.setFieldsValue(user);
    }
  }, [type, UPDATE_TYPE, editedUser]);

  useEffect(() => {
    if (type === CREATE_TYPE) {
      const user = {
        email: undefined,
        is_superuser: false,
        is_active: true,
        is_verified: true,
      };
      form.setFieldsValue(user);
    }
  }, [type, CREATE_TYPE]);

  useEffect(() => {
    const validationKeys = Object.keys(passwordValidationRequirements);
    for (let i = 0; i < validationKeys.length; i += 1) {
      const key = validationKeys[i];
      if (passwordValidationRequirements[key] === false) {
        setValidationStatus('error');
        return;
      }
    }
    setValidationStatus('success');
  }, [passwordValidationRequirements]);

  const createOrUpdateUserRequest = async (payload) => {
    if (type === CREATE_TYPE) {
      return postUser(payload).then((response) => response);
    }
    return patchUser(payload, editedUser.id).then((response) => response);
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch(() => ({ complete: false, values: {} }));

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const { status, data } = await createOrUpdateUserRequest(values);

      if (status === 200 || status === 201) {
        setResponseStatus({ success: true });

        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          setPasswordValidationRequirements({
            length: undefined,
            upperCase: undefined,
            number: undefined,
            specialChar: undefined,
          });
          form.resetFields();
        }, 500);
      } else if (status === undefined) {
        message.error('API appears to be down.', 5);
      } else if (Array.isArray(data?.detail)) {
        setResponseStatus({ success: false, msg: formatErrorMsg(data) });
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

  const getResponseStatus = () => {
    if (responseStatus === null) {
      return null;
    }
    if (responseStatus.success) {
      return (
        <Space>
          <CheckCircleTwoTone style={{ fontSize: 16 }} twoToneColor="#52c41a" />
          <Text style={{ fontSize: 16, whiteSpace: 'normal' }} type="success">
            User
            {' '}
            {type === CREATE_TYPE ? 'created' : 'updated'}
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
    setResponseStatus(null);
    setPasswordValidationRequirements({
      length: undefined,
      upperCase: undefined,
      number: undefined,
      specialChar: undefined,
    });
  };

  const usePasswordIconRender = (isVisible) => {
    if (type !== CREATE_TYPE) return null;
    return isVisible ? <EyeTwoTone /> : <EyeInvisibleOutlined />;
  };

  const getTextType = (validationType) => {
    switch (validationType) {
      case 'length':
        return passwordValidationRequirements.length === undefined ? 'secondary' : passwordValidationRequirements.length ? 'success' : 'danger';
      case 'upperCase':
        return passwordValidationRequirements.upperCase === undefined ? 'secondary' : passwordValidationRequirements.upperCase ? 'success' : 'danger';
      case 'number':
        return passwordValidationRequirements.number === undefined ? 'secondary' : passwordValidationRequirements.number ? 'success' : 'danger';
      case 'specialChar':
        return passwordValidationRequirements.specialChar === undefined ? 'secondary' : passwordValidationRequirements.specialChar ? 'success' : 'danger';
      default:
        return 'secondary';
    }
  };

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Add User' : 'Update User'}
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
          label="User Email"
          name="email"
          rules={[
            {
              required: true,
              message: 'Enter an email',
            },
          ]}
        >
          <Input spellcheck="false" />
        </Form.Item>
        {
          type === CREATE_TYPE ? (
            <Form.Item
              label="Password"
              name="password"
              validateStatus={validationStatus}
              shouldUpdate
              extra={(
                <div style={{ display: 'flex', flexDirection: 'column', marginTop: 8 }}>
                  <Text type={getTextType('length')}>
                    * At least 12 characters.
                  </Text>
                  <Text type={getTextType('upperCase')}>
                    * At least 1 uppercase character.
                  </Text>
                  <Text type={getTextType('number')}>
                    * At least 1 number.
                  </Text>
                  <Text type={getTextType('specialChar')}>
                    * At least 1 special character.
                  </Text>
                </div>
              )}
              rules={[
                {
                  required: true,
                  message: 'Enter a password',
                },
                {
                  validator: async (rule, value) => {
                    if (value === '') {
                      setPasswordValidationRequirements((prevState) => ({
                        ...prevState,
                        length: undefined,
                        upperCase: undefined,
                        number: undefined,
                        specialChar: undefined,
                      }));
                    } else {
                      setPasswordValidationRequirements((prevState) => ({
                        ...prevState,
                        length: value.length > 12,
                        upperCase: /[A-Z]/.test(value),
                        number: /[0-9]/.test(value),
                        specialChar: /[!@#$%^&*()]/.test(value),
                      }));
                    }
                  },
                },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                type="password"
                placeholder="Password"
                iconRender={(isVisible) => usePasswordIconRender(isVisible)}
              />
            </Form.Item>
          ) : null
        }
        <Form.Item
          label="Superuser"
          name="is_superuser"
          valuePropName="checked"
          initialValue={form.getFieldValue('is_superuser')}
          tooltip="Superusers have permissions to add users and configure Swiple. Superuser permissions should be restricted to a small number of people."
        >
          <Checkbox />
        </Form.Item>
        <Form.Item
          label="Active"
          name="is_active"
          valuePropName="checked"
          initialValue={form.getFieldValue('is_active')}
          tooltip="Whether or not the user is active. If not, login and forgot password requests will be denied. Useful if you want to remove a users access but don't want to delete the user."
          hidden={type === CREATE_TYPE}
        >
          <Checkbox />
        </Form.Item>
        <Form.Item
          hidden // Will un-hide once email verification is implemented
          initialValue={form.getFieldValue('is_verified')}
          valuePropName="checked"
          label="Verified"
          name="is_verified"
        >
          <Checkbox />
        </Form.Item>
        <Row style={{ minHeight: 25 }} justify="start" align="top">
          {getResponseStatus()}
        </Row>
      </Form>
    </Modal>
  );
}

UserModal.defaultProps = {
  visible: false,
  editedUser: {},
};

UserModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedUser: PropTypes.objectOf(Object),
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default UserModal;
