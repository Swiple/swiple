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
// Dashboard
// ========================================================

export const getDashboardMetrics = () => axios.get(`${BASE_URL}/dashboard/metrics`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getDashboardIssues = () => axios.get(`${BASE_URL}/dashboard/issue`)
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

export const getDataSourcesJsonSchema = () => axios.get(`${BASE_URL}/datasources/json_schema`)
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
export const getDatasets = (datasourceId) => {
  const params = {};

  if (datasourceId) {
    params.datasource_id = datasourceId;
  }

  return axios.get(
    `${BASE_URL}/dataset`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getDataset = (key) => axios.get(`${BASE_URL}/dataset/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getQuerySample = (data) => axios.post(
  `${BASE_URL}/dataset/sample`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putSample = (key) => axios.put(
  `${BASE_URL}/dataset/sample/${key}`,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postDataset = (data) => axios.post(
  `${BASE_URL}/dataset`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putDataset = (key, data) => axios.put(
  `${BASE_URL}/dataset/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteDataset = (key) => axios.delete(`${BASE_URL}/dataset/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Schedule
// ========================================================
export const getSchedulesJsonSchema = () => axios.get(`${BASE_URL}/schedules/json_schema`)
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
  `${BASE_URL}/schedules/next_run_times`,
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

export const getExpectations = (datasetId, includeHistory = false, datasourceId = null) => {
  const params = {};

  if (datasourceId) {
    params.datasource_id = datasourceId;
  }

  if (datasetId) {
    params.dataset_id = datasetId;
  }

  if (includeHistory) {
    params.include_history = includeHistory;
  }

  return axios.get(
    `${BASE_URL}/expectation`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getExpectation = (key) => axios.get(`${BASE_URL}/expectation/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getExpectationsJsonSchema = () => axios.get(`${BASE_URL}/expectation/json_schema`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postExpectation = (data) => axios.post(
  `${BASE_URL}/expectation`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const putExpectation = (data, key) => axios.put(
  `${BASE_URL}/expectation/${key}`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteExpectation = (key) => axios.delete(`${BASE_URL}/expectation/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

// ========================================================
// Runner
// ========================================================
export const postRunnerValidateDataset = async (data) => axios.post(
  `${BASE_URL}/runner/validate/dataset`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postRunnerExpectation = async (data) => axios.post(
  `${BASE_URL}/runner/validate/expectation`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const postRunnerProfileDataset = async (data) => axios.post(
  `${BASE_URL}/runner/profile/dataset`,
  data,
)
  .then((response) => response)
  .catch((error) => errorHandler(error));
// ========================================================
// Validation
// ========================================================
export const getValidations = () => axios.get(`${BASE_URL}/validation`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const getValidationStats = (datasetId) => axios.get(
  `${BASE_URL}/validation/statistics`,
  { params: { dataset_id: datasetId } },
)
  .then((response) => response)
  .catch((error) => errorHandler(error));

// ========================================================
// Suggestions
// ========================================================
export const getSuggestions = (datasetId, includeHistory = false, datasourceId = null) => {
  const params = {};

  if (datasourceId) {
    params.datasource_id = datasourceId;
  }

  if (datasetId) {
    params.dataset_id = datasetId;
  }

  if (includeHistory) {
    params.include_history = includeHistory;
  }

  return axios.get(
    `${BASE_URL}/suggestion`,
    { params },
  )
    .then((response) => response)
    .catch((error) => errorHandler(error));
};

export const getSuggestion = (key) => axios.get(`${BASE_URL}/suggestion/${key}`)
  .then((response) => response)
  .catch((error) => errorHandler(error));

export const deleteSuggestion = (key) => axios.delete(`${BASE_URL}/suggestion/${key}`)
  .then((data) => data.data)
  .catch((error) => errorHandler(error));

export const enableSuggestion = (key) => axios.post(`${BASE_URL}/suggestion/${key}`)
  .then((response) => response)
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
