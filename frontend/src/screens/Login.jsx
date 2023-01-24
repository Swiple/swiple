import React, { useEffect, useState } from 'react';
import {
  useHistory,
  useLocation,
} from 'react-router-dom';
import {
  Button, Divider, Form, Input, message, Row,
} from 'antd';
import {
  GithubOutlined, LockOutlined, UserOutlined, EyeTwoTone, EyeInvisibleOutlined,
} from '@ant-design/icons';
import {
  Logo,
  GoogleIcon,
  MicrosoftIcon,
  OktaIcon,
} from '../static/images';
import {
  authenticate, getAuthMethods, oauthCallback, login,
} from '../Api';
import { useAuth } from '../Auth';
import { capitalizeFirstLetter } from '../Utils';
import paths from '../config/Routes';

function useQuery() {
  const { search } = useLocation();
  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function Login() {
  const [authMethods, setAuthMethods] = useState([]);
  const [refreshAuthMethods, setRefreshAuthMethods] = useState(true);
  const [refreshOAuthCallback, setRefreshOAuthCallback] = useState(false);
  const [selectedAuthMethod, setSelectedAuthMethod] = useState(null);
  const [loading, setLoading] = useState({});
  const [loginCredentials, setLoginCredentials] = useState(false);
  const [loginDetail, setLoginDetail] = useState(null);
  const [form] = Form.useForm();
  const query = useQuery();
  const history = useHistory();

  const code = query.get('code');
  const provider = query.get('provider');

  const state = query.get('state');
  const auth = useAuth();

  useEffect(() => {
    if (refreshAuthMethods) {
      setRefreshAuthMethods(false);

      // Gets list of configured auth methods. E.g. Username + Password, GitHub, Okta...
      getAuthMethods()
        .then((response) => {
          if (response.status === 200) {
            setAuthMethods(response.data);
          } else if (response.status === 401) {
            // Do nothing
          } else {
            message.error('Failed to get auth methods.', 5);
          }
        });
    }
  }, [refreshAuthMethods, authMethods]);

  useEffect(() => {
    if (selectedAuthMethod !== null) {
      setLoading({ oauth: true });

      // Handles OAuth authentication
      authenticate(selectedAuthMethod)
        .then((response) => {
          if (response.status === 200) {
            window.location.href = response.data.authorization_url;
          } else {
            message.error('Failed to navigate to authentication server.', 5);
            setLoading({ oauth: true });
            setSelectedAuthMethod(null);
          }
        });
    }
  }, [selectedAuthMethod]);

  const getCookie = async (authType) => {
    if (authType === 'usernamepassword') {
      setLoading({ usernamePassword: true });
      return login(form.getFieldsValue());
    }
    return oauthCallback(provider, code, state);
  };

  const loginFailed = () => {
    setLoginDetail({});
    setLoading({});
    message.error('Failed to authenticate.', 5);
    history.replace(paths.LOGIN);
  };

  useEffect(() => {
    if ((code && provider && state && !refreshOAuthCallback) || loginCredentials) {
      const authType = loginCredentials ? 'usernamepassword' : 'oauth';

      setRefreshOAuthCallback(true);
      setLoginCredentials(false);

      getCookie(authType)
        .then((cookieResponse) => {
          if (cookieResponse.status === 200) {
            auth.getUser((response) => {
              if (response.status !== 200) {
                loginFailed();
              }
            });
          } else if (cookieResponse.status === 400) {
            setLoginDetail(cookieResponse.data.detail);
            setLoading({});
            setSelectedAuthMethod(null);
          } else {
            loginFailed();
            setSelectedAuthMethod(null);
          }
        });
    }
  }, [code, history, provider, refreshOAuthCallback, state, loginCredentials]);

  const formFilled = async () => {
    await form.validateFields().then(() => {
      setLoginCredentials(true);
    }).catch(() => {});
  };

  const getLoginDetail = () => {
    if (loginDetail === 'LOGIN_BAD_CREDENTIALS') {
      return 'Email or password is incorrect';
    }

    if (loginDetail === 'LOGIN_USER_NOT_VERIFIED') {
      return 'Email has not been verified.';
    }
    return null;
  };

  const inputIcon = (visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />);

  const usernameAndPassword = () => {
    if (!authMethods.includes('username_and_password')) {
      return null;
    }

    return (
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{ remember: true }}
        size="large"
        form={form}
      >
        <Form.Item
          name="username"
          rules={[{ required: true, message: 'Please input your email.' }]}
        >
          <Input
            prefix={<UserOutlined className="site-form-item-icon" />}
            placeholder="Email"
            type="email"
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: 'Please input your password.' }]}
        >
          <Input.Password
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Password"
            iconRender={() => inputIcon()}
          />
        </Form.Item>
        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            className="login-form-button"
            size="large"
            loading={
              loading?.usernamePassword
            }
            onClick={() => {
              formFilled();
            }}
          >
            Sign In
          </Button>
          <div style={{ marginTop: 20 }} />
          <span style={{ color: '#ff4d4f' }}>{getLoginDetail()}</span>
        </Form.Item>
        <Divider />
      </Form>
    );
  };

  const oauthMethods = () => authMethods.map((authMethod) => {
    if (authMethod === 'username_and_password') return null;
    const meta = {
      github: {
        background: '#333333',
        icon: <GithubOutlined style={{ fontSize: '1.2rem' }} />,
      },
      google: {
        background: '#346DF1',
        icon: (
          <img
            style={{
              width: '1.2rem', height: '1.2rem', marginRight: 10, background: 'white', padding: 2,
            }}
            src={GoogleIcon}
            alt="Google Icon"
          />
        ),
      },
      microsoft: {
        background: '#1A1A1B',
        icon: <img
          style={{
            width: '1.2rem', height: '1.2rem', marginRight: 10,
          }}
          src={MicrosoftIcon}
          alt="Microsoft Icon"
        />,
      },
      okta: {
        background: '#00297A',
        icon: <img
          style={{
            width: '1.2rem', height: '1.2rem', marginRight: 10,
          }}
          src={OktaIcon}
          alt="Okta Icon"
        />,
      },
    };

    const { icon } = meta[authMethod];
    const { background } = meta[authMethod];

    return (
      <Button
        key={authMethod}
        style={{ background, border: 0 }}
        type="primary"
        icon={icon}
        className="auth-methods"
        size="large"
        loading={
          (loading?.oauth && selectedAuthMethod === authMethod)
          || (code !== null && provider === authMethod)
        }
        onClick={() => {
          if (!loading?.oauth) {
            setSelectedAuthMethod(authMethod);
          }
        }}
      >
        Login with
        {' '}
        {capitalizeFirstLetter(authMethod)}
      </Button>
    );
  });

  return (
    <div className="center">
      <Row align="middle" justify="center">
        <img
          style={{ width: 32, height: 32 }}
          src={Logo}
          alt="Logo"
        />
        <span
          style={{
            fontSize: '34px',
            fontWeight: 600,
            position: 'relative',
          }}
        >
          wiple
        </span>
      </Row>
      <Divider>
        <UserOutlined style={{ fontSize: 16, color: '#dedede' }} />
      </Divider>
      {usernameAndPassword()}
      {oauthMethods()}
    </div>
  );
}

export default Login;
