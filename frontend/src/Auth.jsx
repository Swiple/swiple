import React from 'react';
import { Redirect, useHistory, useLocation } from 'react-router-dom';
import paths from './config/Routes';
import { getMe } from './Api';

const AuthContext = React.createContext(null);

// eslint-disable-next-line react/prop-types
export function AuthProvider({ children }) {
  const [user, setUser] = React.useState(undefined);
  const location = useLocation();
  const history = useHistory();

  const signIn = (newUser, callback) => {
    setUser(newUser);
    callback();
  };

  const signOut = (callback) => {
    setUser(null);
    callback();
  };

  const getUser = (callback) => {
    getMe().then((response) => {
      if (response.status === 200) {
        signIn(response.data, () => {
          // Forward user to DASHBOARD screen if they are on LOGIN screen and "from"
          // doesn't exist in state. Forward user to previous screen if "from" exists in state.
          if (response.status === 200 && location.pathname === paths.LOGIN) {
            history.replace(location.state?.from || paths.DASHBOARD);
          }
        });
      }
      callback(response);
    });
  };

  React.useEffect(() => {
    getUser((response) => {
      if (response.status === 401) {
        setUser(null);
        if (location.pathname !== paths.LOGIN) {
          // Redirect unauthorized user to LOGIN screen if they aren't already on it,
          // include current screen in state so we can forward user back to it once they login
          history.push({
            pathname: paths.LOGIN,
            state: { from: location.pathname },
          });
        }
      }
    });
  }, []);

  // eslint-disable-next-line react/jsx-no-constructed-context-values
  const value = {
    user, signIn, signOut, getUser,
  };

  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return React.useContext(AuthContext);
}

// eslint-disable-next-line react/prop-types
export function RequireAuth({ requiresSuperUser, children }) {
  const auth = useAuth();

  if (!auth.user) {
    return null;
  }
  // Redirect non superuser to DASHBOARD screen if they
  // try to access a screen that requires superuser permissions
  if (requiresSuperUser && !auth.user.is_superuser) {
    return <Redirect to={paths.DASHBOARD} />;
  }

  return children;
}
