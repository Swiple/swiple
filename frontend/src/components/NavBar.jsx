import React from 'react';
import { Link, withRouter } from 'react-router-dom';
import {
  Layout, Menu,
} from 'antd';
import {
  DatabaseOutlined, LineChartOutlined, TableOutlined, NotificationOutlined,
} from '@ant-design/icons';
import PropTypes from 'prop-types';
import paths from '../config/Routes';
import {
  Logo,
} from '../static/images';

const { Sider } = Layout;

const NavBar = withRouter((props) => {
  const authPaths = [paths.LOGIN, paths.REGISTER];
  if (authPaths.includes(props.location.pathname)) return null;

  const menuItems = {
    1: {
      title: 'Dashboard',
      pathName: [paths.DASHBOARD],
      icon: <LineChartOutlined />,
    },
    2: {
      title: 'Data Sources',
      pathName: [paths.DATA_SOURCES],
      icon: <DatabaseOutlined />,
    },
    3: {
      title: 'Datasets',
      pathName: [paths.DATASETS, paths.DATASET],
      icon: <TableOutlined />,
    },
    4: {
      title: 'Destinations',
      pathName: [paths.DESTINATIONS],
      icon: <NotificationOutlined />,
    },
  };

  let activeMenu = '1';
  const menus = Object.entries(menuItems).map(([key, value]) => {
    if (value.pathName.includes(props.location.pathname)) {
      activeMenu = key;
    }
    return (
      <Menu.Item key={key} icon={value.icon}>
        <Link to={value.pathName[0]}>
          {value.title}
        </Link>
      </Menu.Item>
    );
  });

  return (
    <Sider
      collapsible
      collapsed={props.collapsed}
      onCollapse={props.onCollapse}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
      }}
    >
      <Menu theme="dark" mode="inline" style={{ margin: '6px 0 6px 0' }} selectable={false}>
        <Menu.Item
          className="slogo"
          key="mail"
          style={{
            fontSize: '20px', fontWeight: 700, color: 'white', cursor: 'default',
          }}
          icon={(
            <img
              style={{ width: 22, height: 22 }}
              src={Logo}
              alt="Logo"
            />
          )}
        >
          wiple
        </Menu.Item>
      </Menu>

      <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} selectedKeys={[activeMenu]}>
        {menus}
      </Menu>
    </Sider>
  );
});

NavBar.propTypes = {
  onCollapse: PropTypes.func.isRequired,
};

export default NavBar;
