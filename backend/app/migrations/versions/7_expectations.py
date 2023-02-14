from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.EXPECTATION_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "create_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
            },
            "dataset_id": {
                "type": "keyword"
            },
            "datasource_id": {
                "type": "keyword"
            },
            "expectation_type": {
                "type": "keyword"
            },
            "kwargs": {
                "type": "text"
            },
            "modified_date": {
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
