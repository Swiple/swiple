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

export default splitDatasetResource;
