import React from 'react';
import { useLocation } from 'react-router-dom';
import { Layout as AntDLayout } from 'antd';
import AvatarDropdown from './AvatarDropdown';

const { Header: AntDHeader } = AntDLayout;

function Header() {
  const location = useLocation();
  const publicRoutes = ['/login'];

  return (
    <div>
      {
      !publicRoutes.includes(location.pathname)
        ? (
          <AntDHeader
            className="site-layout-background"
            style={{
              padding: 0, paddingLeft: 16, paddingRight: 16, background: '#FFFFFF',
            }}
          >
            <div style={{ float: 'right' }}>
              <AvatarDropdown />
            </div>
          </AntDHeader>
        )
        : null
      }
    </div>
  );
}

export default Header;
