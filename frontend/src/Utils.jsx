const splitDatasetResource = (dataset) => {
  let datasetSchema;
  let datasetName;
  let isVirtual;

  if (dataset && dataset.runtime_parameters) {
    datasetSchema = dataset.runtime_parameters.schema;
    datasetName = dataset.dataset_name;
    isVirtual = true;
  } else if (dataset.dataset_name) {
    const splitDataset = dataset.dataset_name.split('.');
    ([datasetSchema, datasetName] = splitDataset);
    isVirtual = false;
  }

  return {
    datasetSchema,
    datasetName,
    isVirtual,
  };
};

/**
 * Takes in a 422 response object in the structure
 * {detail: [
 *   0: {
 *     loc: ["body", "trigger", "InternalTrigger", "end_date"],
 *     msg: "end_date should not be before start_date"
 *   }
 * ]}
 * @param errorResponse
 */
const formatErrorMsg = (errorResponse) => {
  const { detail } = errorResponse;

  return detail.map((errorItem) => {
    const field = errorItem.loc[errorItem.loc.length - 1];
    const { msg } = errorItem;
    return `${field}: ${msg}`;
  });
};

export { formatErrorMsg, splitDatasetResource };
