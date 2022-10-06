import {
  Button, Dropdown, Layout, Menu, message, Modal, Row, Table, Typography,
} from 'antd';
import {
  DeleteFilled, EditFilled, EllipsisOutlined, ExclamationCircleOutlined, PlusOutlined,
} from '@ant-design/icons';
import { v4 as uuidv4 } from 'uuid';
import React, { useEffect, useState } from 'react';
import moment from 'moment';
import Section from '../../components/Section';
import DestinationModal, { CREATE_TYPE, UPDATE_TYPE } from './components/DestinationModal';
import { deleteDestination, getDestinations } from '../../Api';
import { getDestinationIcon } from '../../Utils';

const { Content } = Layout;
const { Title } = Typography;
const { confirm } = Modal;

export default function destinationOverview() {
  const [destinationModal, setDestinationModal] = useState({ visible: false, type: '' });
  const [refreshDestinations, setRefreshDestinations] = useState(true);
  const [destinations, setDestinations] = useState([]);

  useEffect(() => {
    if (refreshDestinations) {
      getDestinations()
        .then((response) => {
          if (response.status === 200) {
            setDestinations(response.data);
          } else {
            message.error('An error occurred while retrieving destinations.', 5);
          }
          setRefreshDestinations(false);
        });
    }
  }, [refreshDestinations, setRefreshDestinations]);

  const openDestinationModal = (modalType, record = null) => {
    let destination = null;
    if (modalType === UPDATE_TYPE) {
      [destination] = destinations.filter((item) => item.key === record.key);
    }

    setDestinationModal({
      visible: true, type: modalType, destination,
    });
  };

  const removeDestination = (row) => new Promise((resolve, reject) => {
    deleteDestination(row.key).then(() => {
      setDestinations(destinations.filter((item) => item.key !== row.key));
      resolve();
    }).catch(() => reject());
  });

  const showDeleteModal = (record) => {
    confirm({
      title: 'Delete Destination',
      icon: <ExclamationCircleOutlined />,
      content: 'Are you sure you would like to delete this Destination?',
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeDestination(record);
      },
      onCancel() {},
    });
  };

  const destinationMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openDestinationModal(UPDATE_TYPE, record)}
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

  const columns = [
    {
      title: 'Destination Name',
      dataIndex: 'destination_name',
    },
    {
      title: 'Destination Type',
      dataIndex: ['kwargs', 'destination_type'],
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
      dataIndex: 'destination',
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
                Destinations
              </Title>
              <Button
                className="card-list-button-dark"
                style={{ fontWeight: 'bold' }}
                type="primary"
                icon={<PlusOutlined />}
                size="medium"
                onClick={() => openDestinationModal(CREATE_TYPE)}
              >
                Destination
              </Button>
              <DestinationModal
                visible={destinationModal.visible}
                type={destinationModal.type}
                editedDestination={destinationModal.destination}
                onCancel={() => {
                  setDestinationModal({
                    visible: false, type: '', team_name: null, members: [],
                  });
                }}
                onFormSubmit={() => {
                  setDestinationModal({
                    visible: false, type: '', team_name: null, members: [],
                  });
                  setRefreshDestinations(true);
                }}
              />
            </Row>
          </Typography>
          <Table
            columns={columns}
            dataSource={destinations}
            pagination={{ position: ['bottomRight'] }}
            rowKey={() => uuidv4()}
          />
        </>
      </Section>
    </Content>
  );
}
