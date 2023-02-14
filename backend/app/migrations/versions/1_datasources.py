from opensearch_reindexer.base import BaseMigration, Config, Language
from app.settings import settings

REINDEX_BODY = {
    "source": {"index": None},
    "dest": {"index": settings.DATASOURCE_INDEX},
}
DESTINATION_INDEX_BODY = {
    "mappings": {
        "properties": {
            "account_name": {
                "type": "keyword"
            },
            "create_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
            },
            "created_by": {
                "type": "keyword"
            },
            "database": {
                "type": "keyword"
            },
            "dataset": {
                "type": "keyword"
            },
            "datasource_name": {
                "fielddata": True,
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                },
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "engine": {
                "type": "keyword"
            },
            "gcp_project": {
                "type": "keyword"
            },
            "host": {
                "type": "keyword"
            },
            "modified_date": {
                "format": "yyyy-MM-dd HH:mm:ss.SSSSSSZZZZZ",
                "type": "date"
            },
            "password": {
                "type": "keyword"
            },
            "port": {
                "type": "integer"
            },
            "region": {
                "type": "keyword"
            },
            "role_name": {
                "type": "keyword"
            },
            "s3_staging_dir": {
                "type": "keyword"
            },
            "schema_name": {
                "type": "keyword"
            },
            "ssl_mode": {
                "type": "boolean"
            },
            "username": {
                "type": "keyword"
            },
            "warehouse": {
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
