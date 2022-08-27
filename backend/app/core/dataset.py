from app.models.dataset import Dataset


def split_dataset_resource(dataset: Dataset):
    if dataset and dataset.runtime_parameters:
        dataset_schema = dataset.runtime_parameters.schema_name
        dataset_name = dataset.dataset_name
        is_virtual = True
    else:
        split_dataset = dataset.dataset_name.split(".")
        dataset_schema, dataset_name = split_dataset
        is_virtual = False

    return dataset_schema, dataset_name, is_virtual
