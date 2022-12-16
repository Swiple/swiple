const axiosDefault = require('axios').default;

const axios = axiosDefault.create({
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});
const BASE_URL = process.env.REACT_APP_API_DOMAIN;

function errorHandler(error) {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.log(error.response.data);
    console.log(error.response.status);
    console.log(error.response.headers);

    // Send to login page if not authenticated
    if (error.response.status === 401) {
      console.log(window.location.pathname);
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      } else {
        return error.response;
      }
      return null;
    }
    return error.response;
  }
  if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    console.log(error.request);
    return {
      status: undefined,
      data: undefined,
    };
  }
  // Something happened in setting up the request that triggered an Error
  console.log('Error', error.message);
  return null;
}

// ========================================================
// Metrics
// ========================================================

export const getResourceCounts = () => axios.get(`${BASE_URL}/metrics/resource-counts`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getTopIssues = () => axios.get(`${BASE_URL}/metrics/top-issues`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Datasource
// ========================================================

export const getDataSources = () => axios.get(`${BASE_URL}/datasources`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDataSource = (key) => axios.get(`${BASE_URL}/datasources/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDataSourcesJsonSchema = () => axios.get(`${BASE_URL}/datasources/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postDataSource = (data) => axios.post(
  `${BASE_URL}/datasources`,
  data,
  { params: { test: true } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putDataSource = (data, key) => axios.put(
  `${BASE_URL}/datasources/${key}`,
  data,
  { params: { test: true } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteDataSource = (key) => axios.delete(`${BASE_URL}/datasources/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

// ========================================================
// Dataset
// ========================================================
export const getDatasetJsonSchema = () => axios.get(`${BASE_URL}/datasets/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDatasets = (datasourceId) => {
  const params = {};

  if (datasourceId) {
    params.datasource_id = datasourceId;
  }

  return axios.get(
    `${BASE_URL}/datasets`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getDataset = (key) => axios.get(`${BASE_URL}/datasets/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getQuerySample = (data) => axios.post(
  `${BASE_URL}/datasets/sample`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putSample = (key) => axios.put(
  `${BASE_URL}/datasets/${key}/sample`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postDataset = (data) => axios.post(
  `${BASE_URL}/datasets`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putDataset = (key, data) => axios.put(
  `${BASE_URL}/datasets/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteDataset = (key) => axios.delete(`${BASE_URL}/datasets/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postRunnerValidateDataset = async (datasetId) => axios.post(
  `${BASE_URL}/datasets/${datasetId}/validate`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const suggestExpectations = (datasetId) => axios.post(
  `${BASE_URL}/datasets/${datasetId}/suggest`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Schedule
// ========================================================
export const getSchedulesJsonSchema = () => axios.get(`${BASE_URL}/schedules/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getSchedulesForDataset = (datasetId) => axios.get(
  `${BASE_URL}/schedules`,
  { params: { dataset_id: datasetId } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postSchedule = (data, datasetId) => axios.post(
  `${BASE_URL}/schedules`,
  data,
  { params: { dataset_id: datasetId } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putSchedule = (data, scheduleId) => axios.put(
  `${BASE_URL}/schedules/${scheduleId}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteSchedule = (key) => axios.delete(`${BASE_URL}/schedules/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postGenerateNextRunTimes = (data) => axios.post(
  `${BASE_URL}/schedules/next-run-times`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Introspect
// ========================================================

export const getSchemas = (datasourceId) => axios.get(
  `${BASE_URL}/introspect/schema`,
  { params: { datasource_id: datasourceId } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getTables = (datasourceId, schema) => axios.get(
  `${BASE_URL}/introspect/table`,
  { params: { datasource_id: datasourceId, schema } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getColumns = (datasourceId, schema, table) => axios.get(
  `${BASE_URL}/introspect/column`,
  {
    params: {
      datasource_id: datasourceId,
      schema,
      table,
    },
  },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Expectations
// ========================================================

export const getExpectations = (
  datasetId,
  datasourceId = null,
  includeHistory = false,
  suggested = null,
  enabled = true,
) => {
  const params = {
    suggested,
    enabled,
  };

  if (datasourceId) {
    params.datasource_id = datasourceId;
  }

  if (datasetId) {
    params.dataset_id = datasetId;
  }

  if (includeHistory) {
    params.include_history = true;
  }

  return axios.get(
    `${BASE_URL}/expectations`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getExpectationsJsonSchema = () => axios.get(`${BASE_URL}/expectations/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postExpectation = (data) => axios.post(
  `${BASE_URL}/expectations`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const enableExpectation = (key) => axios.put(
  `${BASE_URL}/expectations/${key}/enable`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putExpectation = (data, key) => axios.put(
  `${BASE_URL}/expectations/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteExpectation = (key) => axios.delete(`${BASE_URL}/expectations/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

// ========================================================
// Validation
// ========================================================
export const getValidationStats = (datasetId) => axios.get(
  `${BASE_URL}/validations/statistics`,
  { params: { dataset_id: datasetId } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Destinations
// ========================================================

export const getDestinationsJsonSchema = () => axios.get(`${BASE_URL}/destinations/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDestinations = () => axios.get(`${BASE_URL}/destinations`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDestination = (key) => axios.get(`${BASE_URL}/destinations/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postDestination = (data) => axios.post(
  `${BASE_URL}/destinations`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putDestination = (data, key) => axios.put(
  `${BASE_URL}/destinations/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteDestination = (key) => axios.delete(`${BASE_URL}/destinations/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

// ========================================================
// Actions
// ========================================================

export const getActionsJsonSchema = () => axios.get(`${BASE_URL}/actions/json-schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getActions = (resourceKey) => {
  const params = {};

  if (resourceKey) {
    params.resource_key = resourceKey;
  }
  return axios.get(
    `${BASE_URL}/actions`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getAction = (key) => axios.get(`${BASE_URL}/actions/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postAction = (data) => axios.post(
  `${BASE_URL}/actions`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putAction = (data, key) => axios.put(
  `${BASE_URL}/actions/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteAction = (key) => axios.delete(`${BASE_URL}/actions/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

// ========================================================
// Auth
// ========================================================
export const login = (usernamePassword) => axios.post(`${BASE_URL}/auth/login`, new URLSearchParams(usernamePassword), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const logout = () => axios.post(`${BASE_URL}/auth/logout`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getAuthMethods = () => axios.get(`${BASE_URL}/auth/methods`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const authenticate = (path) => axios.get(`${BASE_URL}/auth/${path}/authorize?authentication_backend=cookie`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const oauthCallback = (provider, code, state) => axios.get(
  `${BASE_URL}/auth/${provider}/callback?code=${code}&state=${state}`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Users
// ========================================================
export const getMe = () => axios.get(`${BASE_URL}/user/me`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getUsers = () => axios.get(`${BASE_URL}/user`)
  .then((response) => response)
  .catch((error) => errorHandler(error));
