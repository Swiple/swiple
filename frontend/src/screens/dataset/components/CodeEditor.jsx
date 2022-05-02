import React from 'react';
import PropTypes from 'prop-types';
import Editor from '@uiw/react-textarea-code-editor';

function CodeEditor({
  value, readOnly,
}) {
  const textRef = React.useRef();
  const [code, setCode] = React.useState(value);
  return (
    <Editor
      readOnly={readOnly}
      value={code}
      ref={textRef}
      language="sql"
      placeholder="Please enter JS code."
      onChange={(evn) => setCode(evn.target.value)}
      padding={15}
      style={{
        backgroundColor: '#f5f5f5',
        fontFamily:
          'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
        fontSize: 16,
        borderRadius: '8px',
        maxWidth: '1200px',
      }}
    />
  );
}

CodeEditor.defaultProps = {
  readOnly: false,
  value: '',
};

CodeEditor.propTypes = {
  readOnly: PropTypes.bool,
  value: PropTypes.string,
};

export default CodeEditor;
