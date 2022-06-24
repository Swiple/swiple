import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Collapse, Form, DatePicker, Input, Radio,
  InputNumber, message, Modal, Row, Col, Space, Typography, Table,
} from 'antd';
import { CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import { v4 as uuidv4 } from 'uuid';
import moment from 'moment';
import {
  postSchedule, putSchedule, postGenerateNextRunTimes,
} from '../../../Api';
import AsyncButton from '../../../components/AsyncButton';
import { formatErrorMsg } from '../../../Utils';

const { Text } = Typography;
const { Panel } = Collapse;

export const CREATE_TYPE = 'CREATE';
export const UPDATE_TYPE = 'UPDATE';

function ScheduleModal({
  visible, type, editedSchedule, trigger, datasetId, onCancel, onFormSubmit,
}) {
  if (!visible) {
    return null;
  }

  const [selectedTrigger, setSelectedTrigger] = useState(trigger || 'cron');
  const [responseStatus, setResponseStatus] = useState(null);
  const [nextRunTimes, setNextRunTimes] = useState([]);
  const [refreshNextRunTimes, setRefreshNextRunTimes] = useState(false);

  const [form] = Form.useForm();

  useEffect(() => {
    if (type === UPDATE_TYPE && editedSchedule !== null) {
      const schedule = {
        trigger: {
          ...editedSchedule.trigger,
          start_date: editedSchedule.trigger.start_date
            ? moment(editedSchedule.trigger.start_date) : null,
          end_date: editedSchedule.trigger.end_date
            ? moment(editedSchedule.trigger.end_date) : null,
        },
        misfire_grace_time: editedSchedule.misfire_grace_time,
        max_instances: editedSchedule.max_instances,
      };

      if (editedSchedule.trigger.trigger === 'date' && editedSchedule.trigger?.run_date) {
        schedule.trigger.run_date = moment(schedule.trigger.run_date);

        delete schedule.trigger.start_date;
        delete schedule.trigger.end_date;
      }

      form.setFieldsValue(schedule);

      if (schedule.trigger.trigger !== 'date') {
        setRefreshNextRunTimes(true);
      }
      setSelectedTrigger(trigger);
    }
  }, [type, UPDATE_TYPE, editedSchedule]);

  const createOrUpdateScheduleRequest = async (payload) => {
    const data = payload;
    data.trigger.trigger = selectedTrigger;
    delete data.id;

    if (type === CREATE_TYPE) {
      return postSchedule(payload, datasetId).then((response) => response);
    }
    return putSchedule(payload, editedSchedule.id).then((response) => response);
  };

  const isFormComplete = async () => form.validateFields()
    .then((values) => ({ complete: true, values }))
    .catch((validationInfo) => {
      console.log('Validations failed: ', validationInfo);
      return { complete: false, values: {} };
    });

  useEffect(() => {
    if (refreshNextRunTimes) {
      setRefreshNextRunTimes(false);

      const generateRunTimeDates = async () => {
        const { complete } = await isFormComplete();

        if (complete) {
          const data = form.getFieldsValue(true);
          data.trigger.trigger = selectedTrigger;
          postGenerateNextRunTimes(data)
            .then((response) => {
              if (response.status === 200) {
                const times = response.data.map((runTime, index) => (
                  [index, runTime]
                ));
                setNextRunTimes(times);
                setResponseStatus(null);
              } else if (response.status === 422) {
                setResponseStatus({ success: false, msg: formatErrorMsg(response.data) });
              } else {
                message.error('An error occurred while retrieving next run times.', 5);
                setResponseStatus(null);
              }
            });
        }
      };

      generateRunTimeDates();
    }
  }, [refreshNextRunTimes, setRefreshNextRunTimes]);

  const onFormSubmitInternal = async () => {
    const { complete, values } = await isFormComplete();
    if (complete) {
      const { status, data } = await createOrUpdateScheduleRequest(values);

      if (status === 200) {
        setResponseStatus({ success: true });

        setTimeout(() => {
          // event callback to parent
          onFormSubmit();
          setResponseStatus(null);
          setSelectedTrigger('');
          form.resetFields();
        }, 500);
      } else if (status === 422) {
        setResponseStatus({ success: false, msg: formatErrorMsg(data) });
      } else if (status === undefined) {
        message.error('API appears to be down.', 5);
      } else {
        message.error('An unknown error occurred.', 5);
      }
    } else {
      setResponseStatus(null);
    }
    return null;
  };

  const cronColumns = [
    {
      title: 'Second',
      dataIndex: 'second',
    },
    {
      title: 'Minute',
      dataIndex: 'minute',
    },
    {
      title: 'Hour',
      dataIndex: 'hour',
    },
    {
      title: 'Day',
      dataIndex: 'day',
    },
    {
      title: 'Week',
      dataIndex: 'week',
    },
    {
      title: 'Day Of Week',
      dataIndex: 'day_of_week',
    },
    {
      title: 'Month',
      dataIndex: 'month',
    },
    {
      title: 'Year',
      dataIndex: 'year',
    },
    {
      title: 'Meaning',
      dataIndex: 'meaning',
    },
  ];

  const cronExamples = [
    {
      second: '0', minute: '0', hour: '10', day: '*', week: '*', day_of_week: '*', month: '*', year: '*', meaning: 'Run at 10:00 am (UTC+0) every day',
    },
    {
      second: '0', minute: '15', hour: '12', day: '*', week: '*', day_of_week: '*', month: '*', year: '*', meaning: 'Run at 12:15 pm (UTC+0) every day',
    },
    {
      second: '0', minute: '0', hour: '18', day: '*', week: '*', day_of_week: 'MON-FRI', month: '*', year: '*', meaning: 'Run at 6:00 pm (UTC+0) every Monday through Friday',
    },
    {
      second: '0', minute: '0', hour: '8', day: '1', week: '*', day_of_week: '*', month: '*', year: '*', meaning: 'Run at 8:00 am (UTC+0) every 1st day of the month',
    },
    {
      second: '0', minute: '0/15', hour: '*', day: '*', week: '*', day_of_week: '*', month: '*', year: '*', meaning: 'Run every 15 minutes',
    },
    {
      second: '0', minute: '0/10', hour: '*', day: '*', week: '*', day_of_week: 'MON-FRI', month: '*', year: '*', meaning: 'Run every 10 minutes Monday through Friday',
    },
    {
      second: '0', minute: '0/5', hour: '8-17', day: '*', week: '*', day_of_week: 'MON-FRI', month: '*', year: '*', meaning: 'Run every 5 minutes Monday through Friday between 8:00 am and 5:55 pm (UTC+0)',
    },
  ];

  const buildScheduleForm = () => {
    if (selectedTrigger === 'cron') {
      return (
        <Col>
          <Row>
            <Space>
              <Form.Item
                name={['trigger', 'second']}
                label="Second"
                tooltip="second (0-59)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'minute']}
                label="Minute"
                tooltip="minute (0-59)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'hour']}
                label="Hour"
                tooltip="hour (0-23)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'day']}
                label="Day"
                tooltip="day of month (1-12)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'week']}
                label="Week"
                tooltip="ISO week (1-53)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'day_of_week']}
                label="Day Of Week"
                tooltip="Number or name of weekday (0-5 or mon,tue,wed,thu,fri,sat,sun)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'month']}
                label="Month"
                tooltip="month (1-12)"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                name={['trigger', 'year']}
                label="Year"
                tooltip="4-digit year"
                rules={[{ required: true, message: '' }]}
              >
                <Input />
              </Form.Item>
            </Space>
          </Row>
          <Row>
            <Collapse style={{ width: '100%', marginBottom: 20 }}>
              <Panel header="Examples">
                <Table
                  size="small"
                  columns={cronColumns}
                  dataSource={cronExamples}
                  rowKey={() => uuidv4()}
                  pagination={false}
                />
              </Panel>
            </Collapse>
          </Row>
        </Col>
      );
    }
    if (selectedTrigger === 'interval') {
      return (
        <Row>
          <Space>
            <Form.Item
              name={['trigger', 'seconds']}
              label="Seconds"
              tooltip="Number of seconds to wait"
            >
              <InputNumber />
            </Form.Item>
            <Form.Item
              name={['trigger', 'minutes']}
              label="Minutes"
              tooltip="Number of minutes to wait"
            >
              <InputNumber />
            </Form.Item>
            <Form.Item
              name={['trigger', 'hours']}
              label="Hours"
              tooltip="Number of hours to wait"
            >
              <InputNumber />
            </Form.Item>
            <Form.Item
              name={['trigger', 'days']}
              label="Days"
              tooltip="Number of days to wait"
            >
              <InputNumber />
            </Form.Item>
            <Form.Item
              name={['trigger', 'weeks']}
              label="Weeks"
              tooltip="Number of weeks to wait"
            >
              <InputNumber />
            </Form.Item>
          </Space>
        </Row>
      );
    }
    if (selectedTrigger === 'date') {
      return (
        <Form.Item
          name={['trigger', 'run_date']}
          label="Run Date (Local time zone)"
          tooltip="The date/time to run the job at"
        >
          <DatePicker
            showTime
          />
        </Form.Item>
      );
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
          <Text style={{ fontSize: 16, whiteSpace: 'normal' }} type="success">Schedule looks good!</Text>
        </Space>
      );
    }
    if (!responseStatus.success) {
      let messages;

      if (Array.isArray(responseStatus.msg)) {
        messages = responseStatus.msg.map((msg) => (
          <div style={{ fontSize: 16, color: '#FF4D4F', whiteSpace: 'normal' }}>{msg}</div>
        ));
      } else {
        messages = <Text style={{ fontSize: 16, color: '#FF4D4F', whiteSpace: 'normal' }}>{responseStatus.msg}</Text>;
      }

      return (
        <Space>
          <Row>
            <CloseCircleTwoTone style={{ fontSize: 16, marginTop: 5, marginRight: 5 }} twoToneColor="#FF4D4F" />
            <Col>
              {messages}
            </Col>
          </Row>
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
    setSelectedTrigger('');
  };

  return (
    <Modal
      title={type === CREATE_TYPE ? 'Create Schedule' : 'Update Schedule'}
      visible={visible}
      onCancel={() => {
        onCancelInternal();
        return onCancel();
      }}
      width={1000}
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
        name="dynamic_form_nest_item"
        form={form}
        layout="vertical"
        size="large"
        preserve={false}
        onValuesChange={(changedValues) => {
          if (selectedTrigger !== 'date' && !changedValues?.trigger?.trigger) {
            setRefreshNextRunTimes(true);
          }

          if (changedValues?.trigger?.trigger) {
            setResponseStatus(null);
          }
        }}
      >
        <Form.Item
          name={['trigger', 'trigger']}
          label="Schedule Type"
          initialValue={selectedTrigger}
          rules={[{ required: true, message: 'Select an schedule type.' }]}
        >
          <Radio.Group
            onChange={({ target: { value } }) => {
              setSelectedTrigger(value);
              setNextRunTimes([]);
            }}
            optionType="button"
            buttonStyle="solid"
          >
            <Radio.Button value="cron">
              Cron
            </Radio.Button>
            <Radio.Button value="interval">Interval</Radio.Button>
            <Radio.Button value="date">Date</Radio.Button>
          </Radio.Group>
        </Form.Item>
        {buildScheduleForm()}
        {
          selectedTrigger !== 'date'
            ? (
              <Col style={{ marginBottom: 20 }}>
                <Row style={{ marginBottom: 10 }}>Next 10 trigger dates</Row>
                {
                  nextRunTimes.length === 0
                    ? (
                      <Text italic>
                        Scheduled dates will be generated
                        here upon receiving a valid cron expression
                      </Text>
                    )
                    : nextRunTimes.map(([index, runTime]) => (
                      <Row key={index}>{moment(runTime).local().format('ddd, D MMM YYYY HH:mm:ss Z')}</Row>
                    ))
                }
              </Col>
            )
            : null
        }
        {
          selectedTrigger !== 'date'
            ? (
              <Row>
                <Space size="large">
                  <Form.Item
                    name={['trigger', 'start_date']}
                    label="Start Date (Local time zone)"
                    tooltip="Earliest possible date/time to trigger on (inclusive)"
                  >
                    <DatePicker
                      showTime
                    />
                  </Form.Item>
                  <Form.Item
                    name={['trigger', 'end_date']}
                    label="End Date (Local time zone)"
                    tooltip="Latest possible date/time to trigger on (inclusive)"
                    rules={[
                      {
                        validator: async (rule, value) => {
                          const values = form.getFieldsValue(true);
                          if (value && values.trigger.start_date
                            && value < values.trigger.start_date) {
                            throw new Error('End Date should not be before Start Date');
                          }
                        },
                      },
                    ]}
                  >
                    <DatePicker
                      showTime
                    />
                  </Form.Item>
                </Space>
              </Row>
            ) : null
        }
        <Form.Item
          name="misfire_grace_time"
          label="Misfire Grace Time"
          tooltip="The amount of time (in seconds) that this job’s execution is allowed to be late"
          initialValue={300}
        >
          <InputNumber />
        </Form.Item>
        <Form.Item
          name="max_instances"
          label="Max Instances"
          tooltip="The maximum number of concurrently executing instances allowed for this job"
          initialValue={1}
        >
          <InputNumber />
        </Form.Item>
        <Row style={{ minHeight: 25 }} justify="start" align="top">
          {getResponseStatus()}
        </Row>
      </Form>
    </Modal>
  );
}

ScheduleModal.defaultProps = {
  visible: false,
  editedSchedule: {},
  trigger: '',
};

ScheduleModal.propTypes = {
  visible: PropTypes.bool,
  type: PropTypes.oneOf(['', CREATE_TYPE, UPDATE_TYPE]).isRequired,
  editedSchedule: PropTypes.objectOf(Object),
  trigger: PropTypes.string,
  datasetId: PropTypes.string.isRequired,
  onCancel: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

export default ScheduleModal;
