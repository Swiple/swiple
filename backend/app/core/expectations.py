from great_expectations.core.expectation_configuration import ExpectationConfiguration
from app.models import expectation as exp
from app.utils import json_schema_to_single_doc


def supported_unsupported_expectations():
    supported_expectations = []
    unsupported_expectations = []

    for expectation in exp.type_map.values():
        json_schema = json_schema_to_single_doc(expectation.schema())
        expectation_type = json_schema['properties']['expectation_type']['default']
        supported_expectations.append(expectation_type)

    ge_expectations = ExpectationConfiguration.kwarg_lookup_dict.keys()

    for ge_expectation in ge_expectations:
        if ge_expectation not in supported_expectations:
            unsupported_expectations.append(ge_expectation)

    return {
        'supported_expectations': supported_expectations,
        'unsupported_expectations': unsupported_expectations,
    }