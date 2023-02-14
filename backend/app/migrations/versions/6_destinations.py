from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.DESTINATION_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "destination_name": {
                "fielddata": True,
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                },
                "type": "text"
            },
            "destination_type": {
                "fielddata": True,
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                },
                "type": "text"
            },
            "kwargs": {
                "type": "object"
            },
            "create_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
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
