from opensearch_reindexer.base import BaseMigration, Config, Language

# number of documents to index at a time
BATCH_SIZE = 1000
SOURCE_INDEX = ""
DESTINATION_INDEX = ""
DESTINATION_INDEX_BODY = None


class Migration(BaseMigration):
    def transform_document(self, doc: dict) -> dict:
        # Modify this method to transform each document before being inserted into destination index.
        return doc


config = Config(
    source_index=SOURCE_INDEX,
    destination_index=DESTINATION_INDEX,
    batch_size=BATCH_SIZE,
    destination_index_body=DESTINATION_INDEX_BODY,
    language=Language.python,
)

    