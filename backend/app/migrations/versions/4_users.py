from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.USER_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "oauth_accounts": {
                "type": "nested"
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
