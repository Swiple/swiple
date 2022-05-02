import React from 'react';
import { Avatar, Dropdown, Menu } from 'antd';
import { UserOutlined, CaretDownOutlined } from '@ant-design/icons';
import { useHistory } from 'react-router-dom';
import { logout } from '../Api';

function AvatarDropdown() {
  const history = useHistory();

  const menu = (
    <Menu>
      <Menu.Item
        key="1"
        onClick={() => logout().then((response) => {
          if (response.status === 200) {
            history.replace('/login');
          }
        })}
      >
        Sign Out
      </Menu.Item>
    </Menu>
  );

  return (
    <Dropdown
      overlayStyle={{ marginTop: 50 }}
      overlay={menu}
      placement="bottomLeft"
      arrow
    >
      <div>
        <Avatar icon={<UserOutlined />} />
        <CaretDownOutlined style={{ color: '#CCCCCC' }} />
      </div>
    </Dropdown>
  );
}

export default AvatarDropdown;
