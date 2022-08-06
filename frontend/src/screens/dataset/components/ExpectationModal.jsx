import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Checkbox, Col, Form, Input, InputNumber, message, Row, Select, Space, Typography,
} from 'antd';
import { CheckCircleTwoTone, CloseCircleTwoTone, InfoCircleOutlined } from '@ant-design/icons';
import AsyncButton from '../../../components/AsyncButton';
import Modal from '../../../components/Modal';
import {
  getExpectationsJsonSchema,
  postExpectation, putExpectation,
} from '../../../Api';

const { Option } = Select;
const { Text } = Typography;

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function ExpectationModal({
  visible, type, editedExpectation, dataset, onCancel, onFormSubmit,
}) {
  if (!visible) {
    return null;
  }
  const [expectationsJsonSchema, setExpectationsJsonSchema] = useState([]);
  const [refreshExpectationsJsonSchema, setRefreshExpectationsJsonSchema] = useState(true);
  const [selectedExpectation, setSelectedExpectation] = useState(null);
  const [responseStatus, setResponseStatus] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    if (type === UPDATE_TYPE && editedExpectation !== null && expectationsJsonSchema.length !== 0) {
      setSelectedExpectation(editedExpectation.expectation_type);

      // flatten expectation model for form
      const formData = {
        expectation_type: editedExpectation.expectation_type,
        ...editedExpectation.kwargs,
      };

      form.setFieldsValue(formData);
    }
  }, [type, UPDATE_TYPE, editedExpectation, expectationsJsonSchema]);

  useEffect(() => {
    if (refreshExpectationsJsonSchema && visible) {
      getExpectationsJsonSchema()
        .then((response) => {
          if (response.status === 200) {
            const { data } = response;
            setExpectationsJsonSchema(data);
            setRefreshExpectationsJsonSchema(false);
          } else {
            message.error('An error occurred while retrieving data sources schema.', 5);
          }
        });
    }
  }, [refreshExpectationsJsonSchema, setRefreshExpectationsJsonSchema, visible]);

  if (!visible || type === null) return null;

  const expectationOptions = expectationsJsonSchema.map((item) => (
    <Option
      key={item.title}
      value={item.properties.expectation_type.default}
      label={item.title}
      title={item.title}
      className="select-option-border-bottom"
    >
      <Col className="select-with-text-wrap" align="start" style={{ alignItems: 'center', color: 'black' }}>
        <div><Text strong style={{ fontSize: 18 }}>{item.title}</Text></div>
        <div style={{ marginTop: 10 }} />
        <div>{item.description}</div>
      </Col>
    </Option>
  ));

  const getFormItem = (item, prop, requiredKwargs) => {
    let itemType;

    if (item?.form_type === 'column_select' && dataset.sample?.columns) {
      const datasetSampleColumns = dataset.sample.columns.map((column) => (
        { label: column, value: column }));

      itemType = <Select options={datasetSampleColumns} />;
    } else if (item?.form_type === 'column_select') {
      itemType = <Input placeholder={item.title} />;
    } else if (item?.form_type === 'multi_column_select' && dataset.sample?.columns) {
      const datasetSampleColumns = dataset.sample.columns.map((column) => (
        { label: column, value: column }));

      itemType = <Select mode="multiple" allowClear options={datasetSampleColumns} />;
    } else if (item.type === 'boolean') {
      itemType = <Checkbox />;
    } else if (item.type === 'string') {
      itemType = <Input placeholder={item.title} />;
    } else if (item.type === 'array') {
      itemType = (
        <Select
          mode="tags"
          allowClear
          placeholder={'Type values followed by "Enter"'}
          notFoundContent={null}
        />
      );
    } else if (item.type === 'number' && prop === 'objective') {
      itemType = <InputNumber min={0} max={1} placeholder={0.95} />;
    } else if (item.type === 'integer' || item.type === 'number') {
      itemType = <InputNumber />;
    }

    const rule = item.type === 'boolean'
    || (item.type !== 'boolean' && !requiredKwargs.includes(prop))
      ? null
      : [{ required: true, message: `${item.title} is required` }];

    return (
      <Form.Item
        key={prop}
        label={item.title}
        name={prop}
        rules={rule}
        valuePropName={item.type === 'boolean' ? 'checked' : undefined}
        initialValue={item.type === 'boolean' ? false : undefined}
        tooltip={{ title: item.description, icon: <InfoCircleOutlined /> }}
      >
        {itemType}
      </Form.Item>
    );
  };

  const ignoredProps = ['catch_exceptions', 'include_config', 'result_format'];

  const buildExpectationsOptions = () => {
    if (!selectedExpectation || expectationsJsonSchema.length === 0) {
      return null;
    }
    const expectation = expectationsJsonSchema.filter((item) => (
      item.properties.expectation_type.default === selectedExpectation))[0];
    const kwargProps = expectation.properties.kwargs.properties;
    const requiredKwargs = expectation.properties.kwargs.required;

    return Object.keys(kwargProps).map((prop) => {
      if (!ignoredProps.includes(prop)) {
        return getFormItem(kwargProps[prop], prop, requiredKwargs);
      }
      return null;
    });
  };

  const isFormComplete = () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch((validationInfo) => {
      console.log('Validations failed: ', validationInfo);
      return { complete: false, values: {} };
    });

  const clean = (obj) => {
    const objCopy = obj;
    Object.keys(objCopy).forEach((key) => {
      if (objCopy[key] === null || objCopy[key] === undefined) {
        delete objCopy[key];
      }
    });
    return objCopy;
  };

  const transformExpectationsPayload = (payload) => {
    const cleanedPayload = clean(payload);

    const expectation = expectationsJsonSchema.filter((item) => (
      item.properties.expectation_type.default === payload.expectation_type))[0].properties;
    delete cleanedPayload.expectation_type;

    return {
      datasource_id: dataset.datasource_id,
      dataset_id: dataset.key,
      expectation_type: expectation.expectation_type.default,
      kwargs: {
        ...cleanedPayload,
      },
    };
  };

  const createOrUpdateExpectationRequest = async (payload) => {
    if (type === CREATE_TYPE) {
      return postExpectation(payload).then((response) => response);
    }
    return putExpectation(payload, editedExpectation.key).then((response) => response);
  };

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const transformedValues = transformExpectationsPayload(values);
      const { status, data } = await createOrUpdateExpectationRequest(transformedValues);

      if (status === 200) {
        setResponseStatus({ success: true });

        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          setSelectedExpectation(null);
          form.resetFields();
        }, 500);
      } else if (status === undefined) {
        message.error('API appears to be down.', 5);
      } else if (data?.detail !== undefined) {
        setResponseStatus({ success: false, msg: JSON.stringify(data.detail) });
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

  const onCancelInternal = () => {
    // parent event callback
    onCancel();
    setResponseStatus(null);
    setSelectedExpectation(null);
    form.resetFields();
  };

  if (!visible || type === null) return null;

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Expectation' : 'Update Expectation'}
      visible={visible}
      onCancel={() => {
        onCancelInternal();
        return onCancel();
      }}
      width={800}
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
          name="expectation_type"
          label="Expectation Type"
          rules={[{ required: true, message: 'Select a Expectation.' }]}
        >
          <Select
            showSearch
            placeholder={`Select an expectation (${expectationOptions.length})`}
            onChange={(value) => {
              setSelectedExpectation(value);
            }}
            filterOption={(input, option) => (
              option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0
            )}
          >
            {expectationOptions}
          </Select>
        </Form.Item>
        {buildExpectationsOptions()}
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

ExpectationModal.defaultProps = {
  visible: false,
  editedExpectation: {},
  dataset: {},
};

ExpectationModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedExpectation: PropTypes.objectOf(Object),
  dataset: PropTypes.objectOf(Object),
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default ExpectationModal;
