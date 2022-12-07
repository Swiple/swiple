const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv();

addFormats(ajv);
ajv.addKeyword('placeholder');
ajv.addKeyword('form_type');

const buildValidationErrors = (errorList) => {
  let errorString = '';
  for (let i = 0; i < errorList.length; i += 1) {
    const { message } = errorList[i];
    if (message && !message.includes('unknown keyword')) {
      errorString += `${message}\n`;
    }
  }
  return errorString;
};

export const validateAgainstJsonSchema = (jsonSchema, value) => {
  const validate = ajv.compile(jsonSchema);
  const valid = validate(value);
  if (value !== undefined && !valid) {
    throw new Error(buildValidationErrors(validate.errors));
  }
};

export default ajv;
