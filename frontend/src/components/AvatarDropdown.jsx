import React from 'react';
import { Avatar, Dropdown, Menu } from 'antd';
import { UserOutlined, CaretDownOutlined } from '@ant-design/icons';
import { logout } from '../Api';
import paths from '../config/Routes';

function AvatarDropdown() {
  const menu = (
    <Menu>
      <Menu.Item
        key="1"
        onClick={() => logout().then((response) => {
          if (response.status === 200) {
            window.location.href = paths.LOGIN;
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
