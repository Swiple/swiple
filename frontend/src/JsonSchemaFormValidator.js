const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv();

addFormats(ajv);
ajv.addKeyword('placeholder');

export default ajv;
