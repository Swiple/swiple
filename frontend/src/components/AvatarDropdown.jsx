import React from 'react';
import {
  Avatar, Dropdown, Menu, Space,
} from 'antd';
import Text from 'antd/es/typography/Text';
import { logout } from '../Api';
import paths from '../config/Routes';
import { useAuth } from '../Auth';

function AvatarDropdown() {
  const auth = useAuth();

  return (
    <Dropdown
      trigger={['click']}
      overlay={(
        <Menu>
          <Menu.Item
            key="1"
            style={{ borderBottom: '1px solid #F0F0F0', cursor: 'auto', backgroundColor: '#fff' }}
          >
            <Text style={{ color: '#001529', fontWeight: 'bold' }}>
              {auth.user?.email}
            </Text>
          </Menu.Item>
          <Menu.Item
            key="2"
            onClick={() => logout().then((response) => {
              if (response.status === 200) {
                window.location.href = paths.LOGIN;
              }
            })}
          >
            <Text>
              Sign Out
            </Text>
          </Menu.Item>
        </Menu>
      )}
      placement="bottomRight"
      arrow
    >
      <Space style={{ cursor: 'pointer' }}>
        <Avatar style={{ backgroundColor: '#001529', color: 'white' }}>
          {auth.user?.email[0].toUpperCase()}
        </Avatar>
        <Text style={{ color: '#001529' }}>
          {auth.user?.email.split('@')[0]}
        </Text>
      </Space>
    </Dropdown>
  );
}

export default AvatarDropdown;
