import { Card } from 'antd';
import React from 'react';
import PropTypes from 'prop-types';

const renderTotal = (total) => {
  if (!total && total !== 0) {
    return null;
  }

  let totalDom;

  const totalStyle = {
    height: '38px',
    marginTop: '4px',
    marginBottom: 0,
    overflow: 'hidden',
    color: 'rgba(0, 0, 0, 0.85)',
    fontSize: '30px',
    lineHeight: '38px',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    wordBreak: 'break-all',
  };

  switch (typeof total) {
    case 'undefined':
      totalDom = null;
      break;

    case 'function':
      totalDom = <div style={totalStyle}>{total()}</div>;
      break;

    default:
      totalDom = <div style={totalStyle}>{total}</div>;
  }

  return totalDom;
};

function ChartCard({
  contentHeight, title, total, children, loading, ...rest
}) {
  const renderContent = () => {
    if (loading) {
      return false;
    }

    return (
      <div style={{ position: 'relative' }}>
        <div
          style={{ position: 'relative', width: '100%', overflow: 'hidden' }}
        >
          <div style={{ float: 'left' }}>
            <div style={{
              height: '22px', color: 'rgba(0, 0, 0, 0.45)', fontSize: '14px', lineHeight: '22px',
            }}
            >
              <span>{title}</span>
            </div>
            {renderTotal(total)}
          </div>
        </div>
        {children && (
          <div
            style={{
              position: 'relative',
              width: '100%',
              marginBottom: '12px',
              height: contentHeight || 'auto',
            }}
          >
            <div
              style={{
                position: 'absolute', bottom: 0, left: 0, width: '100%',
              }}
              className={contentHeight}
            >
              {children}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <Card
      loading={loading}
      bodyStyle={{
        padding: '20px 24px 8px 24px',
      }}
      {...rest}
    >
      {renderContent()}
    </Card>
  );
}

ChartCard.defaultProps = {
  total: null,
};

ChartCard.propTypes = {
  contentHeight: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  total: PropTypes.number,
  children: PropTypes.element.isRequired,
  loading: PropTypes.bool.isRequired,
};

export default ChartCard;
