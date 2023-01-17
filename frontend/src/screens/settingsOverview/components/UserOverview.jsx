import {
  Button, Dropdown, Menu, message, Modal, Row, Table, Typography,
} from 'antd';
import {
  DeleteFilled,
  EditFilled,
  EllipsisOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
  CloseSquareOutlined,
  CheckSquareOutlined,
} from '@ant-design/icons';
import { v4 as uuidv4 } from 'uuid';
import React, { useEffect, useState } from 'react';
import Section from '../../../components/Section';
import UserModal, { CREATE_TYPE, UPDATE_TYPE } from './UserModal';
import { deleteUser, getUsers } from '../../../Api';

const { Title } = Typography;
const { confirm } = Modal;

export default function userOverview() {
  const [userModal, setUserModal] = useState({ visible: false, type: '' });
  const [refreshUsers, setRefreshUsers] = useState(true);
  const [users, setUsers] = useState([]);

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

  const openUserModal = (modalType, record = null) => {
    let user = null;
    if (modalType === UPDATE_TYPE) {
      [user] = users.filter((item) => item.email === record.email);
    }

    setUserModal({
      visible: true, type: modalType, user,
    });
  };

  const removeUser = (row) => new Promise((resolve, reject) => {
    deleteUser(row.id).then(() => {
      setUsers(users.filter((item) => item.id !== row.id));
      resolve();
    }).catch(() => reject());
  });

  const showDeleteModal = (record) => {
    confirm({
      title: 'Delete User',
      icon: <ExclamationCircleOutlined />,
      content: 'Are you sure you would like to delete this User?',
      okText: 'Delete',
      okType: 'danger',
      onOk() {
        return removeUser(record);
      },
      onCancel() {},
    });
  };

  const userMenu = (record) => (
    <Menu>
      <Menu.Item
        key="1"
        icon={<EditFilled />}
        onClick={() => openUserModal(UPDATE_TYPE, record)}
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

  const checkOrCross = (text) => (text ? <CheckSquareOutlined style={{ fontSize: 18, color: '#52C41A' }} /> : <CloseSquareOutlined style={{ fontSize: 18, color: '#FF4D4F' }} />);

  const columns = [
    {
      title: 'Email',
      dataIndex: 'email',
    },
    {
      title: 'Superuser',
      dataIndex: 'is_superuser',
      render: (text) => checkOrCross(text),
    },
    {
      title: 'Active',
      dataIndex: 'is_active',
      render: (text) => checkOrCross(text),
    },
    {
      title: 'Verified',
      dataIndex: 'is_verified',
      render: (text) => checkOrCross((text)),
    },
    {
      title: '',
      render: (text, record) => (
        <Dropdown
          trigger={['click']}
          overlay={userMenu(record)}
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
              Users
            </Title>
            <Button
              className="card-list-button-dark"
              style={{ fontWeight: 'bold' }}
              type="primary"
              icon={<PlusOutlined />}
              size="medium"
              onClick={() => openUserModal(CREATE_TYPE)}
            >
              User
            </Button>
            <UserModal
              visible={userModal.visible}
              type={userModal.type}
              editedUser={userModal.user}
              onCancel={() => {
                setUserModal({
                  visible: false, type: '',
                });
              }}
              onFormSubmit={() => {
                setUserModal({
                  visible: false, type: '',
                });
                setRefreshUsers(true);
              }}
            />
          </Row>
        </Typography>
        <Table
          columns={columns}
          dataSource={users}
          pagination={{ position: ['bottomRight'] }}
          rowKey={() => uuidv4()}
        />
      </>
    </Section>
  );
}
