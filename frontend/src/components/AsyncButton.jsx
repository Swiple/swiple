import React, { useEffect, useState } from 'react';
import { Button } from 'antd';
import PropTypes from 'prop-types';

function isPromise(value) {
  // ref: https://stackoverflow.com/questions/27746304/how-do-i-tell-if-an-object-is-a-promise

  return (
    typeof value === 'object'
    && value !== null
    && 'then' in value
    && typeof value.then === 'function'
  );
}

export default function AsyncButton({ onClick, loading: primitiveLoading, ...restProps }) {
  const [isHandlingClick, setHandlingClick] = useState(false);
  const [clickArgs, setClickArgs] = useState(undefined);

  useEffect(() => {
    let mounted = true;

    (async () => {
      if (typeof onClick === 'function' && !isHandlingClick && clickArgs) {
        const returnValue = onClick(...clickArgs);

        if (isPromise(returnValue)) {
          // If "onClick" function return a Promise
          // According to the status of Promise, switch loading automatically.
          try {
            setHandlingClick(true);
            await returnValue;
            if (mounted) {
              setHandlingClick(false);
            }
          } catch (e) {
            if (mounted) {
              setHandlingClick(false);
            }
            throw e;
          }
        }
      }
    })();

    // eslint-disable-next-line no-return-assign
    return () => mounted = false;
  }, [clickArgs]);

  return (
    <Button
      {...restProps}
      loading={primitiveLoading === undefined ? isHandlingClick : primitiveLoading}
      onClick={async (...args) => {
        setClickArgs(args);
      }}
    />
  );
}

AsyncButton.defaultProps = {
  loading: undefined,
};

AsyncButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};
