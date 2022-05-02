import React, { useState } from 'react';
import { Layout as AntDLayout } from 'antd';
import PropTypes from 'prop-types';
import NavBar from './NavBar';
import Header from './Header';

function Layout({ children }) {
  const [collapsed, setCollapsed] = useState(false);

  const onCollapse = () => {
    setCollapsed(!collapsed);
  };

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
