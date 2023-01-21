import React, {} from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import './App.css';
import Routes from './Routes';
import Layout from './components/Layout';
import { AuthProvider } from './Auth';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Routes />
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;
