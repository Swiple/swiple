import json

import openmock
from openmock.utilities import extract_ignore_as_iterable
from opensearchpy.client.utils import query_params
from opensearchpy.exceptions import NotFoundError


class FakeOpenSearch(openmock.FakeOpenSearch):
    """openmock.FakeOpenSearch completed with some missing methods we use."""

    @query_params(
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "default_operator",
        "df",
        "expand_wildcards",
        "ignore_throttled",
        "ignore_unavailable",
        "lenient",
        "min_score",
        "preference",
        "q",
        "routing",
        "terminate_after",
    )
    def count(self, body=None, index=None, doc_type=None, params=None, headers=None):
        results = self.search(
            index, doc_type=doc_type, body=body, params=params, headers=headers
        )

        result = {
            "count": results["hits"]["total"]["value"],
            "_shards": {"successful": 1, "skipped": 0, "failed": 0, "total": 1},
        }

        return result

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "if_primary_term",
        "if_seq_no",
        "lang",
        "refresh",
        "require_alias",
        "retry_on_conflict",
        "routing",
        "timeout",
        "wait_for_active_shards",
    )
    def update(self, index, id, body, doc_type="_doc", params=None, headers=None):
        found = False
        result = None
        version = None
        ignore = extract_ignore_as_iterable(params)

        if index in self.__documents_dict:
            for document in self.__documents_dict[index]:
                if document.get("_id") == id:
                    found = True
                    if doc_type and document.get("_type") != doc_type:
                        found = False
                    if found:
                        doc = self.get(index, id, doc_type=doc_type, params=params)
                        version = doc["_version"] + 1
                        self.delete(index, id, doc_type=doc_type)
                        result = "updated"
                        self.__documents_dict[index].append(
                            {
                                "_type": doc_type,
                                "_id": id,
                                "_source": body["doc"],
                                "_index": index,
                                "_version": version,
                            }
                        )

        result_dict = {
            "_index": index,
            "_type": doc_type,
            "_id": id,
            "_version": version,
            "result": result,
            "get": {
                "_source": body["doc"],
            },
        }

        if found:
            return result_dict
        elif params and 404 in ignore:
            return {"found": False}
        else:
            raise NotFoundError(404, json.dumps(result_dict))

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "conflicts",
        "default_operator",
        "df",
        "expand_wildcards",
        "from_",
        "ignore_unavailable",
        "lenient",
        "max_docs",
        "preference",
        "q",
        "refresh",
        "request_cache",
        "requests_per_second",
        "routing",
        "scroll",
        "scroll_size",
        "search_timeout",
        "search_type",
        "size",
        "slices",
        "sort",
        "stats",
        "terminate_after",
        "timeout",
        "version",
        "wait_for_active_shards",
        "wait_for_completion",
    )
    def delete_by_query(self, index, body, doc_type=None, params=None, headers=None):
        total_deleted = 0
        if isinstance(index, list):
            (index,) = index
        matches = self.search(
            index=index, doc_type=doc_type, body=body, params=params, headers=headers
        )
        if matches["hits"]["total"]:
            for hit in matches["hits"]["hits"]:
                self.delete(index, id=hit["_id"], doc_type=hit["_type"])
                total_deleted += 1

        return {
            "took": 1,
            "time_out": False,
            "total": matches["hits"]["total"],
            "updated": 0,
            "deleted": total_deleted,
            "batches": 1,
            "version_conflicts": 0,
            "noops": 0,
            "retries": 0,
            "throttled_millis": 100,
            "requests_per_second": 100,
            "throttled_until_millis": 0,
            "failures": [],
        }
