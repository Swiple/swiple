from typing import Optional, List, Any
from pydantic import Field
from app.models.base_model import BaseModel
from app import constants as c
from enum import Enum


class IgnoreRowIf(str, Enum):
    both_values_are_missing = "both_values_are_missing"
    either_value_is_missing = "either_value_is_missing"
    neither = "neither"


class Expectation(BaseModel):
    dataset_id: str
    datasource_id: str
    expectation_type: str
    kwargs: dict
    meta: Optional[dict]
    create_date: Optional[str]
    modified_date: Optional[str]


class ExpectColumnToExist(BaseModel):
    """
    Expect the specified column to exist.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        column_index: Optional[int] = Field(description=c.COLUMN_INDEX)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_TO_EXIST
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect column "{self.kwargs.column}" to exist.'


class ExpectTableColumnsToMatchOrderedList(BaseModel):
    """
    Expect the columns to exactly match a specified list.
    """
    class Kwargs(BaseModel):
        column_list: List[str] = Field(description=c.COLUMN_LIST, form_type="multi_column_select")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_COLUMNS_TO_MATCH_ORDERED_LIST
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect order of columns to match list {self.kwargs.column_list}.'


class ExpectTableColumnsToMatchSet(BaseModel):
    """
    Expect the columns to match a specified set.
    """

    class Kwargs(BaseModel):
        column_set: List[str] = Field(description=c.COLUMN_SET, form_type="multi_column_select")
        exact_match: bool = Field(description=c.EXACT_MATCH)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_COLUMNS_TO_MATCH_SET
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect columns to match set {self.kwargs.column_set}'


# TODO make min max values conditionally optional
class ExpectTableRowCountToBeBetween(BaseModel):
    """
    Expect the number of rows to be between two values.
    """
    class Kwargs(BaseModel):
        min_value: int = Field(description="The minimum number of rows, inclusive. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has no minimum.")
        max_value: int = Field(description="The maximum number of rows, inclusive. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has no maximum.")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_ROW_COUNT_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect table row count to be between {self.kwargs.min_value} and {self.kwargs.max_value}.'


class ExpectTableRowCountToEqual(BaseModel):
    """
    Expect the number of rows to equal a value.
    """
    class Kwargs(BaseModel):
        value: int = Field(description="The expected number of rows.")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_ROW_COUNT_TO_EQUAL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect the number of rows to equal {self.kwargs.value}.'


class ExpectTableColumnCountToBeBetween(BaseModel):
    """
    Expect the number of columns to be between two values.
    """
    class Kwargs(BaseModel):
        min_value: int = Field(description="The minimum number of columns, inclusive. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable columns.")
        max_value: int = Field(description="The maximum number of columns, inclusive. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable columns.")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_COLUMN_COUNT_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect table column count to be between {self.kwargs.min_value} and {self.kwargs.max_value}.'


class ExpectTableColumnCountToBeEqual(BaseModel):
    """
    Expect the number of columns to equal a value.
    """
    class Kwargs(BaseModel):
        value: int = Field(description="The expected number of columns.")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_TABLE_COLUMN_COUNT_TO_EQUAL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect table column count to equal {self.kwargs.value}.'


class ExpectColumnValuesToBeUnique(BaseModel):
    """
    Expect each column value to be unique.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_BE_UNIQUE
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect each value in column "{self.kwargs.column}" to be unique.'


class ExpectCompoundColumnsToBeUnique(BaseModel):
    """
    Expect that the columns are unique together, e.g. a multi-column primary key
    """
    class Kwargs(BaseModel):
        column_list: List[str] = Field(description=c.COLUMN_LIST, form_type="multi_column_select")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COMPOUND_COLUMNS_TO_BE_UNIQUE
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect unique combination of values for columns "{self.kwargs.column_list}".'


class ExpectSelectColumnValuesToBeUniqueWithinRecord(BaseModel):
    """
    Expect the values for each record to be unique across the columns listed.
    Note that records can be duplicated.
    """
    class Kwargs(BaseModel):
        column_list: List[str] = Field(description=c.COLUMN_LIST, form_type="multi_column_select")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_SELECT_COLUMN_VALUES_TO_BE_UNIQUE_WITHIN_RECORD
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect the values for each record to be unique across columns "{self.kwargs.column_list}".'


class ExpectColumnValuesToNotBeNull(BaseModel):
    """
    Expect column values to NOT be null. Values must be explicitly null or missing.
    Empty strings don’t count as null unless they have been coerced to a null type.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_NOT_BE_NULL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect values in column "{self.kwargs.column}" to NOT be null or missing.'


class ExpectColumnValuesToBeNull(BaseModel):
    """
    Expect column values to be null.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_BE_NULL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect values in column "{self.kwargs.column}" to be null.'


class ExpectColumnValuesToBeInSet(BaseModel):
    """
    Expect each column value to be in a given set.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        value_set: List[Any] = Field(description=c.VALUE_SET)
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        parse_strings_as_datetimes: Optional[bool] = Field(description=c.PARSE_STRINGS_AS_DATETIMES)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_BE_IN_SET
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect each value in column "{self.kwargs.column}" to exist in set {self.kwargs.value_set}'


class ExpectColumnValuesToNotBeInSet(BaseModel):
    """
    Expect each column value to NOT be in a given set.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        value_set: List[Any] = Field(description=c.VALUE_SET)
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_NOT_BE_IN_SET
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect each value in column "{self.kwargs.column}" to NOT exist in set {self.kwargs.value_set}'


# TODO make min max values conditionally optional, add validators, support cross types
# cross types cause issues in OpenSearch as type return for min/max_value are strings
# instead of floats.
class ExpectColumnValuesToBeBetween(BaseModel):
    """
    Expect column entries to be between a minimum value and a maximum value.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimum value for a column entry. If min_value is None, then max_value is treated as an upper bound, and there is no minimum value checked.")
        max_value: float = Field(description="The maximum value for a column entry. If max_value is None, then min_value is treated as a lower bound, and there is no maximum value checked.")
        strict_min: bool = Field(description="If True, values must be strictly larger than min_value.", default=False)
        strict_max: bool = Field(description="If True, values must be strictly smaller than max_value", default=False)
        # allow_cross_type_comparisons: bool = Field(description="If True, allow comparisons between types (e.g. integer and string). Otherwise, attempting such comparisons will raise an exception.", default=False)
        # parse_strings_as_datetimes: Optional[bool] = Field(description="If True, parse min_value, max_value, and all non-null column values to datetimes before making comparisons.")
        # output_strftime_format: Optional[bool] = Field(description="A valid strfime format for datetime output. Only used if parse_strings_as_datetimes=True.")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries in column "{self.kwargs.column}" to be between {self.kwargs.min_value} and {self.kwargs.max_value}. '


# TODO make min max values conditionally optional
class ExpectColumnValueLengthsToBeBetween(BaseModel):
    """
    Expect column entries to be strings with length between a minimum value and a maximum value.
    This expectation only works for string-type values.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: int = Field(description="The minimum value for a column entry length. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has no minimum.", default=False)
        max_value: int = Field(description="The maximum value for a column entry length. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has no maximum.", default=False)
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUE_LENGTHS_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings with length between {self.kwargs.min_value} value and {self.kwargs.max_value} value (inclusive).'


class ExpectColumnValueLengthsToEqual(BaseModel):
    """
    Expect column entries to be strings with length equal to the provided value.
    This expectation only works for string-type values.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        value: int = Field(description="The expected value for a column entry length.")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUE_LENGTHS_TO_EQUAL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings with length equal to {self.kwargs.value}.'


class ExpectColumnValuesToMatchRegex(BaseModel):
    """
    Expect column entries to be strings that match a given regular expression.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        regex: str = Field(description="The regular expression the column entries should match. Valid matches can be found anywhere in the string, for example “[at]+” will identify the following strings as expected: “cat”, “hat”, “aa”, “a”, and “t”, and the following strings as unexpected: “fish”, “dog”.")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_MATCH_REGEX
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings that match the regular expression "{self.kwargs.regex}".'


class ExpectColumnValuesToNotMatchRegex(BaseModel):
    """
    Expect column entries to be strings that do NOT match a given regular expression. The regex must NOT match any portion of the provided string. .
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        regex: str = Field(description="The regular expression the column entries should NOT match. For example, “[at]+” would identify the following strings as expected: “fish”, “dog”, and the following as unexpected: “cat”, “hat”")
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings that do NOT match the regular expression "{self.kwargs.regex}".'


# TODO check enum works
class ExpectColumnValuesToMatchRegexList(BaseModel):
    """
    Expect the column entries to be strings that can be matched to either any of or all of a list of regular expressions. Matches can be anywhere in the string.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        regex_list: List[str] = Field(description="The list of regular expressions which the column entries should match.")
        match_on: str = Field(
            description="“any” or “all”. Use “any” if the value should match at least one regular expression in the list. Use “all” if it should match each regular expression in the list.",
            enum=["any", "all"]
        )
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_MATCH_REGEX_LIST
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings that can be matched to "{self.kwargs.match_on}" of a list of regular expressions "{self.kwargs.regex_list}".'


# TODO check enum works
class ExpectColumnValuesToNotMatchRegexList(BaseModel):
    """
    Expect the column entries to be strings that do not match any of a list of regular expressions. Matches can be anywhere in the string.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        regex_list: List[str] = Field(description="The list of regular expressions which the column entries should match.")
        match_on: str = Field(
            description="“any” or “all”. Use “any” if the value should match at least one regular expression in the list. Use “all” if it should match each regular expression in the list.",
            enum=["any", "all"]
        )
        mostly: Optional[float] = Field(description=c.MOSTLY, ge=0, le=1)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX_LIST
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect entries for column "{self.kwargs.column}" to be strings that do NOT match "{self.kwargs.match_on}" of a list of regular expressions "{self.kwargs.regex_list}".'


# TODO make min max values conditionally optional
class ExpectColumnMeanToBeBetween(BaseModel):
    """
    Expect the column mean to be between a minimum value and a maximum value (inclusive).
    min_value and max_value are both inclusive unless strict_min or strict_max are set to True.


    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimum value for the column mean. If min_value is None, then max_value is treated as an upper bound.")
        max_value: float = Field(description="The maximum value for the column mean. If max_value is None, then min_value is treated as a lower bound.")
        strict_min: bool = Field(description="If True, the column median must be strictly larger than min value.", default=False)
        strict_max: bool = Field(description="If True, the column median must be strictly smaller than max value.", default=False)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_MEAN_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = less_than + " or equal to"

        return f'Expect the mean for column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value}.'


# TODO make min max values conditionally optional
class ExpectColumnMedianToBeBetween(BaseModel):
    """
    Expect the column median to be between a minimum value and a maximum value.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimum value for the column median. If min_value is None, then max_value is treated as an upper bound.")
        max_value: float = Field(description="The maximum value for the column median. If max_value is None, then min_value is treated as a lower bound.")
        strict_min: bool = Field(description="If True, the column median must be strictly larger than min value.", default=False)
        strict_max: bool = Field(description="If True, the column median must be strictly smaller than max value.", default=False)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_MEDIAN_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = less_than + " or equal to"

        return f'Expect the median for column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value}.'


# TODO make min max values conditionally optional
class ExpectColumnUniqueValueCountToBeBetween(BaseModel):
    """
    Expect the number of unique values to be between a minimum value and a maximum value. (inclusive)
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: int = Field(description="The minimum number of unique values allowed. If min_value is None, then max_value is treated as an upper bound")
        max_value: int = Field(description="The maximum number of unique values allowed. If max_value is None, then min_value is treated as a lower bound")
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_UNIQUE_VALUE_COUNT_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect the number of unique values in column "{self.kwargs.column}" to be greater than or equal to {self.kwargs.min_value} and less than or equal to {self.kwargs.max_value}.'


# TODO make min max values conditionally optional
class ExpectColumnProportionOfUniqueValuesToBeBetween(BaseModel):
    """
    Expect the proportion of unique values to be between a minimum value and a maximum value.
    For example, in a column containing [1, 2, 2, 3, 3, 3, 4, 4, 4, 4], there are 4 unique values and 10 total values for a proportion of 0.4.
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(ge=0, le=1, description="The minimum proportion of unique values. If min_value is None, then max_value is treated as an upper bound.")
        max_value: float = Field(ge=0, le=1, description="The maximum proportion of unique values. If max_value is None, then min_value is treated as a lower bound.")
        strict_min: bool = Field(description="If True, the minimum proportion of unique values must be strictly larger than min value.", default=False)
        strict_max: bool = Field(description="If True, the maximum proportion of unique values must be strictly smaller than max value.", default=False)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_PROPORTION_OF_UNIQUE_VALUES_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = less_than + " or equal to"

        return f'Expect the proportion of unique values for column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value}.'


# TODO make min max values conditionally optional
class ExpectColumnSumToBeBetween(BaseModel):
    """
    Expect the column to sum to be between an min and max value
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimal sum allowed.")
        max_value: float = Field(description="The maximal sum allowed.")
        strict_min: bool = Field(description="If True, the minimal sum must be strictly larger than min value.", default=False)
        strict_max: bool = Field(description="If True, the maximal sum must be strictly smaller than max value.", default=False)
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_SUM_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = greater_than + " or equal to"

        return f'Expect the sum of values for column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value}.'


class ExpectMultiColumnSumToEqual(BaseModel):
    """
    Expect the sum of row values is the same for each row, summing only values in column_list, and equal to sum_total.
    """
    class Kwargs(BaseModel):
        column_list: List[str] = Field(description=c.COLUMN_LIST, form_type="multi_column_select")
        sum_total: int
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_MULTICOLUMN_SUM_TO_EQUAL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect the sum of row values is the same for each row, summing only values in {self.kwargs.column_list}, and equal to {self.kwargs.sum_total}.'


# TODO make min max values conditionally optional
class ExpectColumnMinToBeBetween(BaseModel):
    """
    Expect the column minimum to be between an min and max value
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimal column minimum allowed.")
        max_value: float = Field(description="The maximal column minimum allowed.")
        strict_min: bool = Field(description="If True, the minimal column minimum must be strictly larger than min value.", default=False)
        strict_max: bool = Field(description="If True, the maximal column minimum must be strictly smaller than max value.", default=False)
        parse_strings_as_datetimes: Optional[bool] = Field(description="If True, parse min_value, max_values, and all non-null column values to datetimes before making comparisons.", default=False)
        output_strftime_format: Optional[str] = Field(description="A valid strfime format for datetime output. Only used if parse_strings_as_datetimes=True.")  # TODO validation on "Only used if..."
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_MIN_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"
        parse_strings = "where min, max, and all non-null values are parsed as datetimes before comparison"
        strftime_format = f" with a strftime format of {self.kwargs.output_strftime_format}"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = less_than + " or equal to"
        if not self.kwargs.parse_strings_as_datetimes:
            parse_strings = ""
        if not self.kwargs.output_strftime_format:
            strftime_format = ""

        return f'Expect the minimum value in column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value} {parse_strings} {strftime_format}.'


# TODO make min max values conditionally optional
class ExpectColumnMaxToBeBetween(BaseModel):
    """
    Expect the column maximum to be between an min and max value
    """
    class Kwargs(BaseModel):
        column: str = Field(description=c.COLUMN, form_type="column_select")
        min_value: float = Field(description="The minimal column minimum allowed.")
        max_value: float = Field(description="The maximal column minimum allowed.")
        strict_min: Optional[bool] = Field(description="If True, the minimal column minimum must be strictly larger than min value.", default=False)
        strict_max: Optional[bool] = Field(description="If True, the maximal column minimum must be strictly smaller than max value.", default=False)
        parse_strings_as_datetimes: Optional[bool] = Field(description="If True, parse min_value, max_values, and all non-null column values to datetimes before making comparisons.", default=False)
        output_strftime_format: Optional[str] = Field(description="A valid strfime format for datetime output. Only used if parse_strings_as_datetimes=True.")  # TODO validation on "Only used if..."
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_MAX_TO_BE_BETWEEN
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_AGGREGATE_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        greater_than = "greater than"
        less_than = "less than"
        parse_strings = "where min, max, and all non-null values are parsed as datetimes before comparison"
        strftime_format = f" with a strftime format of {self.kwargs.output_strftime_format}"

        if not self.kwargs.strict_min:
            greater_than = greater_than + " or equal to"
        if not self.kwargs.strict_max:
            less_than = less_than + " or equal to"
        if not self.kwargs.parse_strings_as_datetimes:
            parse_strings = ""
        if not self.kwargs.output_strftime_format:
            strftime_format = ""

        return f'Expect the maximum value in column "{self.kwargs.column}" to be {greater_than} {self.kwargs.min_value} and {less_than} {self.kwargs.max_value} {parse_strings} {strftime_format}.'


class ExpectColumnPairValuesToBeEqual(BaseModel):
    """
    Expect the values in column A to be the same as column B.
    """
    class Kwargs(BaseModel):
        column_A: str = Field(description="The first column name.", form_type="column_select")
        column_B: str = Field(description="The second column name.", form_type="column_select")
        ignore_row_if: str = Field(
            description="Ignore row if.",
            enum=["both_values_are_missing", "either_value_is_missing", "neither"]
        )
        result_format: str = "SUMMARY"
        include_config: bool = True
        catch_exceptions: bool = True

    dataset_id: str
    datasource_id: str
    expectation_type: str = c.EXPECT_COLUMN_PAIR_VALUES_TO_BE_EQUAL
    kwargs: Kwargs
    meta: Optional[dict]
    result_type: str = c.COLUMN_MAP_EXPECTATION
    create_date: Optional[str]
    modified_date: Optional[str]

    def documentation(self):
        return f'Expect values in column "{self.kwargs.column_A}" to be the same as column "{self.kwargs.column_B}" where the row is ignored if {self.kwargs.ignore_row_if}.'


type_map = {
    c.EXPECT_COLUMN_TO_EXIST: ExpectColumnToExist,
    c.EXPECT_TABLE_COLUMNS_TO_MATCH_ORDERED_LIST: ExpectTableColumnsToMatchOrderedList,
    c.EXPECT_TABLE_COLUMNS_TO_MATCH_SET: ExpectTableColumnsToMatchSet,
    c.EXPECT_TABLE_ROW_COUNT_TO_BE_BETWEEN: ExpectTableRowCountToBeBetween,
    c.EXPECT_TABLE_ROW_COUNT_TO_EQUAL: ExpectTableRowCountToEqual,
    c.EXPECT_TABLE_COLUMN_COUNT_TO_BE_BETWEEN: ExpectTableColumnCountToBeBetween,
    c.EXPECT_TABLE_COLUMN_COUNT_TO_EQUAL: ExpectTableColumnCountToBeEqual,
    c.EXPECT_COLUMN_VALUES_TO_BE_UNIQUE: ExpectColumnValuesToBeUnique,
    c.EXPECT_COMPOUND_COLUMNS_TO_BE_UNIQUE: ExpectCompoundColumnsToBeUnique,
    c.EXPECT_SELECT_COLUMN_VALUES_TO_BE_UNIQUE_WITHIN_RECORD: ExpectSelectColumnValuesToBeUniqueWithinRecord,
    c.EXPECT_COLUMN_VALUES_TO_NOT_BE_NULL: ExpectColumnValuesToNotBeNull,
    c.EXPECT_COLUMN_VALUES_TO_BE_NULL: ExpectColumnValuesToBeNull,
    c.EXPECT_COLUMN_VALUES_TO_BE_IN_SET: ExpectColumnValuesToBeInSet,
    c.EXPECT_COLUMN_VALUES_TO_NOT_BE_IN_SET: ExpectColumnValuesToNotBeInSet,
    c.EXPECT_COLUMN_VALUES_TO_BE_BETWEEN: ExpectColumnValuesToBeBetween,
    c.EXPECT_COLUMN_VALUE_LENGTHS_TO_BE_BETWEEN: ExpectColumnValueLengthsToBeBetween,
    c.EXPECT_COLUMN_VALUE_LENGTHS_TO_EQUAL: ExpectColumnValueLengthsToEqual,
    c.EXPECT_COLUMN_VALUES_TO_MATCH_REGEX: ExpectColumnValuesToMatchRegex,
    c.EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX: ExpectColumnValuesToNotMatchRegex,
    c.EXPECT_COLUMN_VALUES_TO_MATCH_REGEX_LIST: ExpectColumnValuesToMatchRegexList,
    c.EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX_LIST: ExpectColumnValuesToNotMatchRegexList,
    c.EXPECT_COLUMN_MEAN_TO_BE_BETWEEN: ExpectColumnMeanToBeBetween,
    c.EXPECT_COLUMN_MEDIAN_TO_BE_BETWEEN: ExpectColumnMedianToBeBetween,
    c.EXPECT_COLUMN_UNIQUE_VALUE_COUNT_TO_BE_BETWEEN: ExpectColumnUniqueValueCountToBeBetween,
    c.EXPECT_COLUMN_PROPORTION_OF_UNIQUE_VALUES_TO_BE_BETWEEN: ExpectColumnProportionOfUniqueValuesToBeBetween,
    c.EXPECT_COLUMN_SUM_TO_BE_BETWEEN: ExpectColumnSumToBeBetween,
    c.EXPECT_MULTICOLUMN_SUM_TO_EQUAL: ExpectMultiColumnSumToEqual,
    c.EXPECT_COLUMN_MIN_TO_BE_BETWEEN: ExpectColumnMinToBeBetween,
    c.EXPECT_COLUMN_MAX_TO_BE_BETWEEN: ExpectColumnMaxToBeBetween,
    c.EXPECT_COLUMN_PAIR_VALUES_TO_BE_EQUAL: ExpectColumnPairValuesToBeEqual,
}
