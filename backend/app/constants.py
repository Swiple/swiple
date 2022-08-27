# APP Type
APP_SWIPLE_API = "SWIPLE_API"
APP_SCHEDULER = "SCHEDULER"

# Expectation Descriptions
COLUMN = "The column to be analyzed."
VALUE_SET = "A comma separated set of values. Remove all unnecessary whitespace."
OBJECTIVE = "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run."
PARSE_STRINGS_AS_DATETIMES = "If True, values provided in Value Set will be parsed as datetimes before making comparisons."
COLUMN_INDEX = "If not None, checks the order of the columns. The expectation will fail if the column is not in location column_index (zero-indexed)."
COLUMN_LIST = "The column names, in the correct order."
COLUMN_SET = "The column names you wish to check. Column names are case sensitive."
EXACT_MATCH = "Whether to make sure there are no extra columns in either the dataset or in the column_set."
MIN_VALUE = ""
MAX_VALUE = ""

# Supported Expectation
EXPECT_COLUMN_TO_EXIST = "expect_column_to_exist"
EXPECT_TABLE_COLUMNS_TO_MATCH_ORDERED_LIST = (
    "expect_table_columns_to_match_ordered_list"
)
EXPECT_TABLE_COLUMNS_TO_MATCH_SET = "expect_table_columns_to_match_set"
EXPECT_TABLE_ROW_COUNT_TO_BE_BETWEEN = "expect_table_row_count_to_be_between"
EXPECT_TABLE_ROW_COUNT_TO_EQUAL = "expect_table_row_count_to_equal"
EXPECT_TABLE_COLUMN_COUNT_TO_BE_BETWEEN = "expect_table_column_count_to_be_between"
EXPECT_TABLE_COLUMN_COUNT_TO_EQUAL = "expect_table_column_count_to_equal"

EXPECT_COLUMN_VALUES_TO_BE_UNIQUE = "expect_column_values_to_be_unique"
EXPECT_COMPOUND_COLUMNS_TO_BE_UNIQUE = "expect_compound_columns_to_be_unique"
EXPECT_SELECT_COLUMN_VALUES_TO_BE_UNIQUE_WITHIN_RECORD = (
    "expect_select_column_values_to_be_unique_within_record"
)
EXPECT_COLUMN_VALUES_TO_NOT_BE_NULL = "expect_column_values_to_not_be_null"
EXPECT_COLUMN_VALUES_TO_BE_NULL = "expect_column_values_to_be_null"
EXPECT_COLUMN_VALUES_TO_BE_IN_SET = "expect_column_values_to_be_in_set"
EXPECT_COLUMN_VALUES_TO_NOT_BE_IN_SET = "expect_column_values_to_not_be_in_set"
EXPECT_COLUMN_VALUES_TO_BE_BETWEEN = "expect_column_values_to_be_between"
EXPECT_COLUMN_VALUE_LENGTHS_TO_BE_BETWEEN = "expect_column_value_lengths_to_be_between"
EXPECT_COLUMN_VALUE_LENGTHS_TO_EQUAL = "expect_column_value_lengths_to_equal"
EXPECT_COLUMN_VALUES_TO_MATCH_REGEX = "expect_column_values_to_match_regex"
EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX = "expect_column_values_to_not_match_regex"
EXPECT_COLUMN_VALUES_TO_MATCH_REGEX_LIST = "expect_column_values_to_match_regex_list"
EXPECT_COLUMN_VALUES_TO_NOT_MATCH_REGEX_LIST = (
    "expect_column_values_to_not_match_regex_list"
)
EXPECT_COLUMN_MEAN_TO_BE_BETWEEN = "expect_column_mean_to_be_between"
EXPECT_COLUMN_MEDIAN_TO_BE_BETWEEN = "expect_column_median_to_be_between"
EXPECT_COLUMN_UNIQUE_VALUE_COUNT_TO_BE_BETWEEN = (
    "expect_column_unique_value_count_to_be_between"
)
EXPECT_COLUMN_PROPORTION_OF_UNIQUE_VALUES_TO_BE_BETWEEN = (
    "expect_column_proportion_of_unique_values_to_be_between"
)
EXPECT_MULTICOLUMN_SUM_TO_EQUAL = "expect_multicolumn_sum_to_equal"
EXPECT_COLUMN_SUM_TO_BE_BETWEEN = "expect_column_sum_to_be_between"
EXPECT_COLUMN_MIN_TO_BE_BETWEEN = "expect_column_min_to_be_between"
EXPECT_COLUMN_MAX_TO_BE_BETWEEN = "expect_column_max_to_be_between"
EXPECT_COLUMN_PAIR_VALUES_TO_BE_EQUAL = "expect_column_pair_values_to_be_equal"

# Types
COLUMN_MAP_EXPECTATION = "column_map_expectation"
COLUMN_AGGREGATE_EXPECTATION = "column_aggregate_expectation"
EXPECTATION = "expectation"

# Scheduler Triggers
INTERVAL = "interval"
CRON = "cron"
DATE = "date"

# Scheduler Descriptions
MAX_INSTANCES = (
    "The maximum number of concurrently executing instances allowed for this schedule"
)
MISFIRE_GRACE_TIME = "The amount of time (in seconds) that this schedule’s execution is allowed to be late"

START_DATE = "Earliest possible date/time to trigger on (inclusive)"
END_DATE = "Latest possible date/time to trigger on (inclusive)"

# CronTrigger
SECOND = "second (0-59)"
MINUTE = "minute (0-59)"
HOUR = "hour (0-23)"
DAY_OF_WEEK = "Number or name of weekday (0-5 or mon,tue,wed,thu,fri,sat,sun)"
WEEK = "ISO week (1-53)"
DAY = "day of month (1-12)"
MONTH = "month (1-12)"
YEAR = "4-digit year"

# IntervalTrigger
SECONDS = "Number of seconds to wait"
MINUTES = "Number of minutes to wait"
HOURS = "Number of hours to wait"
DAYS = "Number of days to wait"
WEEKS = "Number of weeks to wait"

# DateTrigger
RUN_DATE = "The date/time to run the schedule at"
