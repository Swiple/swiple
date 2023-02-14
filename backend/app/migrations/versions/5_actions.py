from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.ACTION_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "resource_key": {
                "type": "keyword"
            },
            "resource_type": {
                "type": "keyword"
            },
            "action_type": {
                "type": "keyword"
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
