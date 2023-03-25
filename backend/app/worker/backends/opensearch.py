"""OpenSearch result store backend."""
from datetime import datetime

from kombu.utils.encoding import bytes_to_str
from kombu.utils.url import _parse_url

from celery import states
from celery.exceptions import ImproperlyConfigured

from celery.backends.base import KeyValueStoreBackend
from app.db.client import client

try:
    import opensearchpy
except ImportError:
    opensearchpy = None

__all__ = ('OpenSearchBackend',)

OS_LIB_MISSING = """\
You need to install the opensearch-py library to use the OpenSearch \
result backend.\
"""


class OpenSearchBackend(KeyValueStoreBackend):
    """OpenSearch result backend.

    Raises:
        celery.exceptions.ImproperlyConfigured:
            if module :pypi:`opensearch-py` is not available.
    """

    index = 'celery'
    doc_type = 'backend'
    scheme = 'http'
    host = 'localhost'
    port = 9200
    username = None
    password = None
    os_retry_on_timeout = False
    os_timeout = 10
    os_max_retries = 3

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        _get = self.app.conf.get

        if opensearchpy is None:
            raise ImproperlyConfigured(OS_LIB_MISSING)

        index = doc_type = scheme = host = port = username = password = None

        if url:
            scheme, host, port, username, password, path, _ = _parse_url(url)
            if scheme == 'opensearch':
                scheme = None
            if path:
                path = path.strip('/')
                index, _, doc_type = path.partition('/')

        self.index = index or self.index
        self.doc_type = doc_type or self.doc_type
        self.scheme = scheme or self.scheme
        self.host = host or self.host
        self.port = port or self.port
        self.username = username or self.username
        self.password = password or self.password

        self.os_retry_on_timeout = (
            _get('opensearch_retry_on_timeout') or self.os_retry_on_timeout
        )

        os_timeout = _get('opensearch_timeout')
        if os_timeout is not None:
            self.os_timeout = os_timeout

        os_max_retries = _get('opensearch_max_retries')
        if os_max_retries is not None:
            self.os_max_retries = os_max_retries

        self.os_save_meta_as_text = _get('opensearch_save_meta_as_text', True)
        self._server = None

    def exception_safe_to_retry(self, exc):
        if isinstance(exc, (opensearchpy.exceptions.TransportError)):
            # 401: Unauthorized
            # 409: Conflict
            # 429: Too Many Requests
            # 500: Internal Server Error
            # 502: Bad Gateway
            # 503: Service Unavailable
            # 504: Gateway Timeout
            # N/A: Low level exception (i.e. socket exception)
            if exc.status_code in {401, 409, 429, 500, 502, 503, 504, 'N/A'}:
                return True
        return False

    def get(self, key):
        try:
            res = self._get(key)
            try:
                if res['found']:
                    return res['_source']['result']
            except (TypeError, KeyError):
                pass
        except opensearchpy.exceptions.NotFoundError:
            pass

    def exception_to_python(self, exc):
        """Overrides base exception_to_python"""
        return exc

    def _get(self, key):
        return self.server.get(
            index=self.index,
            id=key,
        )

    def _set_with_state(self, key, value, state):
        body = {
            'result': value,
            'timestamp': '{}Z'.format(
                datetime.utcnow().isoformat()[:-3]
            ),
        }
        try:
            self._index(
                id=key,
                body=body,
            )
        except opensearchpy.exceptions.ConflictError:
            # document already exists, update it
            self._update(key, body, state)

    def set(self, key, value):
        return self._set_with_state(key, value, None)

    def _index(self, id, body, **kwargs):
        body = {bytes_to_str(k): v for k, v in body.items()}
        return self.server.index(
            id=bytes_to_str(id),
            index=self.index,
            body=body,
            params={'op_type': 'create'},
            **kwargs
        )

    def _update(self, id, body, state, **kwargs):
        """Update state in a conflict free manner.

        If state is defined (not None), this will not update OS server if either:
        * existing state is success
        * existing state is a ready state and current state in not a ready state

        This way, a Retry state cannot override a Success or Failure, and chord_unlock
        will not retry indefinitely.
        """
        body = {bytes_to_str(k): v for k, v in body.items()}

        try:
            res_get = self._get(key=id)
            if not res_get.get('found'):
                return self._index(id, body, **kwargs)
            # document disappeared between index and get calls.
        except opensearchpy.exceptions.NotFoundError:
            return self._index(id, body, **kwargs)

        try:
            meta_present_on_backend = self.decode_result(res_get['_source']['result'])
        except (TypeError, KeyError):
            pass
        else:
            if meta_present_on_backend['status'] == states.SUCCESS:
                # if stored state is already in success, do nothing
                return {'result': 'noop'}
            elif meta_present_on_backend['status'] in states.READY_STATES and state in states.UNREADY_STATES:
                # if stored state is in ready state and current not, do nothing
                return {'result': 'noop'}

        # get current sequence number and primary term
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/optimistic-concurrency-control.html
        seq_no = res_get.get('_seq_no', 1)
        prim_term = res_get.get('_primary_term', 1)

        # try to update document with current seq_no and primary_term
        res = self.server.update(
            id=bytes_to_str(id),
            index=self.index,
            body={'doc': body},
            params={'if_primary_term': prim_term, 'if_seq_no': seq_no},
            **kwargs
        )
        # result is OpenSearch update query result
        # noop = query did not update any document
        # updated = at least one document got updated
        if res['result'] == 'noop':
            raise opensearchpy.exceptions.ConflictError(409, 'conflicting update occurred concurrently', {})
        return res

    def encode(self, data):
        if self.os_save_meta_as_text:
            return super().encode(data)
        else:
            if not isinstance(data, dict):
                return super().encode(data)
            if data.get("result"):
                data["result"] = self._encode(data["result"])[2]
            if data.get("traceback"):
                data["traceback"] = self._encode(data["traceback"])[2]
            return data

    def decode(self, payload):
        if self.os_save_meta_as_text:
            return super().decode(payload)
        else:
            if not isinstance(payload, dict):
                return super().decode(payload)
            if payload.get("result"):
                payload["result"] = super().decode(payload["result"])
            if payload.get("traceback"):
                payload["traceback"] = super().decode(payload["traceback"])
            return payload

    def mget(self, keys):
        return [self.get(key) for key in keys]

    def delete(self, key):
        self.server.delete(index=self.index, id=key)

    def _get_server(self):
        """Connect to the OpenSearch server."""
        http_auth = None
        if self.username and self.password:
            http_auth = (self.username, self.password)
        return client

    @property
    def server(self):
        if self._server is None:
            self._server = self._get_server()
        return self._server
