from typing import get_args

from great_expectations.core.expectation_configuration import ExpectationConfiguration

from app.models.expectation import Expectation
from app.utils import json_schema_to_single_doc


def supported_unsupported_expectations():
    supported_expectations = []
    unsupported_expectations = []

    for expectation in get_args(Expectation):
        json_schema = json_schema_to_single_doc(expectation.schema())
        expectation_type = json_schema['properties']['expectation_type']['value']
        supported_expectations.append(expectation_type)

    ge_expectations = ExpectationConfiguration.kwarg_lookup_dict.keys()

    for ge_expectation in ge_expectations:
        if ge_expectation not in supported_expectations:
            unsupported_expectations.append(ge_expectation)

    return {
        'supported_expectations': supported_expectations,
        'unsupported_expectations': unsupported_expectations,
    }