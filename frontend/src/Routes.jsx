import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import PropTypes from 'prop-types';
import Login from './screens/Login';
import Dashboard from './screens/dashboard';
import DatasourceOverview from './screens/datasourceOverview';
import DatasetOverview from './screens/datasetOverview';
import Dataset from './screens/dataset';
import UserOverview from './screens/settingsOverview';
import { RequireAuth } from './Auth';
import paths from './config/Routes';
import ActionOverview from './screens/destinationOverview';

function PrivateRoute({
  requiresSuperUser, component, path, ...rest
}) {
  return (
    <Route
      {...rest}
      path={path}
      render={() => (
        <RequireAuth
          requiresSuperUser={requiresSuperUser}
        >
          {component}
        </RequireAuth>
      )}
    />
  );
}

PrivateRoute.defaultProps = {
  requiresSuperUser: false,
};

PrivateRoute.propTypes = {
  requiresSuperUser: PropTypes.bool,
  component: PropTypes.element.isRequired,
  path: PropTypes.string.isRequired,
};

function PublicRoute({ component, path, ...rest }) {
  return (
    <Route
      {...rest}
      path={path}
      render={() => component}
    />
  );
}

PublicRoute.propTypes = {
  component: PropTypes.element.isRequired,
  path: PropTypes.string.isRequired,
};

function Routes() {
  return (
    <Switch>
      <PublicRoute
        exact
        path={paths.LOGIN}
        component={<Login />}
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
        requiresSuperUser
        path={paths.SETTINGS}
        component={<UserOverview />}
      />
      <Redirect
        from="*"
        to={paths.DASHBOARD}
      />
    </Switch>
  );
}

export default Routes;
