from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.DATASET_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "create_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
            },
            "created_by": {
                "type": "keyword"
            },
            "data_asset_name": {
                "fielddata": True,
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                },
                "type": "text"
            },
            "dataset_name": {
                "fielddata": True,
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                },
                "type": "text"
            },
            "datasource_id": {
                "type": "keyword"
            },
            "engine": {
                "type": "keyword"
            },
            "modified_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
            },
            "runtime_parameters": {
                "properties": {
                    "query": {
                        "type": "keyword"
                    },
                    "schema": {
                        "type": "keyword"
                    }
                },
                "type": "object"
            }
        }
    }
}


class Migration(BaseMigration):
    def before_revision(self):
        pass

    def after_revision(self):
        pass


config = Config(
    reindex_body=REINDEX_BODY,
    destination_index_body=DESTINATION_INDEX_BODY,
    language=Language.painless,
)
