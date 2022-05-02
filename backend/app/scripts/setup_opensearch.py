import opensearchpy.exceptions
import yaml
from app.db.client import client


def create_indicies(path=f"/code/app/config/opensearch.yaml"):
    indicies = yaml.load(open(path), Loader=yaml.SafeLoader)
    print(indicies)

    for value in indicies.values():
        try:
            response = client.indices.create(
                index=value["index_name"],
                body={
                    "mappings": value["mappings"]
                }
            )
            print(f"Created index {value['index_name']}")
        except opensearchpy.exceptions.RequestError as ex:
            if ex.error == "resource_already_exists_exception":
                pass
            else:
                raise ex


create_indicies()
