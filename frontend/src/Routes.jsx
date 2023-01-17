import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import PropTypes from 'prop-types';
import Login from './screens/Login';
import Dashboard from './screens/dashboard';
import DatasourceOverview from './screens/datasourceOverview';
import DatasetOverview from './screens/datasetOverview';
import Dataset from './screens/dataset';
import UserOverview from './screens/settingsOverview';
import { RequireAuth, AuthProvider } from './Auth';
import paths from './config/Routes';
import ActionOverview from './screens/destinationOverview';

function PrivateRoute({ component, path, ...rest }) {
  return (
    <Route
      {...rest}
      path={path}
      render={() => (
        <RequireAuth>
          {component}
        </RequireAuth>
      )}
    />
  );
}

PrivateRoute.propTypes = {
  component: PropTypes.element.isRequired,
  path: PropTypes.string.isRequired,
};

function Routes() {
  return (
    <AuthProvider>
      <Switch>
        <Route
          exact
          path={paths.LOGIN}
          component={Login}
        />
        <PrivateRoute
          exact
          path={paths.DASHBOARD}
          component={<Dashboard />}
        />
        <PrivateRoute
          exact
          path={paths.DATA_SOURCES}
          component={<DatasourceOverview />}
        />
        <PrivateRoute
          exact
          path={paths.DATASETS}
          component={<DatasetOverview />}
        />
        <PrivateRoute
          exact
          path={paths.DATASET}
          component={<Dataset />}
        />
        <PrivateRoute
          exact
          path={paths.DESTINATIONS}
          component={<ActionOverview />}
        />
        <PrivateRoute
          exact
          path={paths.SETTINGS}
          component={<UserOverview />}
        />
        <Redirect
          from="*"
          to={paths.DASHBOARD}
        />
      </Switch>
    </AuthProvider>
  );
}

export default Routes;
