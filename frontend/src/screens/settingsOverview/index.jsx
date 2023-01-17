import {
  Layout,
} from 'antd';
import React from 'react';
import UserOverview from './components/UserOverview';

const { Content } = Layout;

export default function settingsOverview() {
  return (
    <Content className="site-layout-background">
      <UserOverview />
    </Content>
  );
}
