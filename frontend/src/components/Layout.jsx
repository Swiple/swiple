import React, { useState } from 'react';
import { Layout as AntDLayout, Spin, Row } from 'antd';
import PropTypes from 'prop-types';
import NavBar from './NavBar';
import Header from './Header';
import { useAuth } from '../Auth';

function Layout({ children }) {
  const [collapsed, setCollapsed] = useState(false);
  const auth = useAuth();

  const onCollapse = () => {
    setCollapsed(!collapsed);
  };

  if (auth.user === undefined) {
    return (
      <div className="center-spinner">
        <Row justify="center">
          <Spin size="large" />
        </Row>
      </div>
    );
  }

  return (
    <AntDLayout hasSider>
      <NavBar
        collapsed={collapsed}
        onCollapse={() => onCollapse()}
      />
      <AntDLayout
        className="site-layout"
        style={{
          marginLeft: collapsed ? 80 : 200,
          transition: 'all .2s',
        }}
      >
        <Header />
        { children }
      </AntDLayout>
    </AntDLayout>
  );
}

Layout.propTypes = {
  children: PropTypes.element.isRequired,
};

export default Layout;
