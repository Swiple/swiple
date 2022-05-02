import React from 'react';
import { Redirect, useLocation } from 'react-router-dom';
import paths from './config/Routes';
import { getMe } from './Api';

const AuthContext = React.createContext(null);

const authProvider = {
  isAuthenticated: false,
  signIn(callback) {
    authProvider.isAuthenticated = true;
    setTimeout(callback, 100); // fake async
  },
  signOut(callback) {
    authProvider.isAuthenticated = false;
    setTimeout(callback, 100);
  },
};

// eslint-disable-next-line react/prop-types
export function AuthProvider({ children }) {
  const [user, setUser] = React.useState(null);

  const signIn = (newUser, callback) => authProvider.signIn(() => {
    setUser(newUser);
    callback();
  });

  const signOut = (callback) => authProvider.signOut(() => {
    setUser(null);
    callback();
  });

  // TODO
  // eslint-disable-next-line react/jsx-no-constructed-context-values
  const value = { user, signIn, signOut };

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
export function RequireAuth({ children }) {
  const auth = useAuth();
  const location = useLocation();

  if (location.pathname !== paths.LOGIN && !auth.user) {
    getMe().then((meResponse) => {
      if (meResponse.status === 200) {
        auth.signIn(meResponse.data.email, () => {});
      }
    });
  } else if (!auth.user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Redirect to={paths.LOGIN} state={{ from: location }} replace />;
  }

  return children;
}
