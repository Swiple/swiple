export const jsonSchema = [
  {
    "title": "ExpectColumnToExist",
    "description": "Expect the specified column to exist.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_to_exist",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "column_index": {
            "title": "Column Index",
            "description": "If not None, checks the order of the columns. The expectation will fail if the column is not in location column_index (zero-indexed).",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableColumnsToMatchOrderedList",
    "description": "Expect the columns to exactly match a specified list.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_columns_to_match_ordered_list",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_list": {
            "title": "Column List",
            "description": "The column names, in the correct order.",
            "form_type": "multi_column_select",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_list"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableColumnsToMatchSet",
    "description": "Expect the columns to match a specified set.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_columns_to_match_set",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_set": {
            "title": "Column Set",
            "description": "The column names you wish to check. Column names are case sensitive.",
            "form_type": "multi_column_select",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "exact_match": {
            "title": "Exact Match",
            "description": "Whether to make sure there are no extra columns in either the dataset or in the column_set.",
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_set",
          "exact_match"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableRowCountToBeBetween",
    "description": "Expect the number of rows to be between two values.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_row_count_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "min_value": {
            "title": "Min Value",
            "description": "The minimum number of rows, inclusive. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has no minimum.",
            "type": "integer"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum number of rows, inclusive. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has no maximum.",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableRowCountToEqual",
    "description": "Expect the number of rows to equal a value.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_row_count_to_equal",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "value": {
            "title": "Value",
            "description": "The expected number of rows.",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableColumnCountToBeBetween",
    "description": "Expect the number of columns to be between two values.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_column_count_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "min_value": {
            "title": "Min Value",
            "description": "The minimum number of columns, inclusive. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable columns.",
            "type": "integer"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum number of columns, inclusive. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable columns.",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectTableColumnCountToBeEqual",
    "description": "Expect the number of columns to equal a value.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_table_column_count_to_equal",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "value": {
            "title": "Value",
            "description": "The expected number of columns.",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToBeUnique",
    "description": "Expect each column value to be unique.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_be_unique",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectCompoundColumnsToBeUnique",
    "description": "Expect that the columns are unique together, e.g. a multi-column primary key",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_compound_columns_to_be_unique",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_list": {
            "title": "Column List",
            "description": "The column names, in the correct order.",
            "form_type": "multi_column_select",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_list"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectSelectColumnValuesToBeUniqueWithinRecord",
    "description": "Expect the values for each record to be unique across the columns listed.\nNote that records can be duplicated.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_select_column_values_to_be_unique_within_record",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_list": {
            "title": "Column List",
            "description": "The column names, in the correct order.",
            "form_type": "multi_column_select",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_list"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToNotBeNull",
    "description": "Expect column values to NOT be null. Values must be explicitly null or missing.\nEmpty strings don’t count as null unless they have been coerced to a null type.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_not_be_null",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToBeNull",
    "description": "Expect column values to be null.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_be_null",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToBeInSet",
    "description": "Expect each column value to be in a given set.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_be_in_set",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "value_set": {
            "title": "Value Set",
            "description": "A comma separated set of values. Remove all unnecessary whitespace.",
            "type": "array",
            "items": {}
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "parse_strings_as_datetimes": {
            "title": "Parse Strings As Datetimes",
            "description": "If True, values provided in Value Set will be parsed as datetimes before making comparisons.",
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "value_set"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToNotBeInSet",
    "description": "Expect each column value to NOT be in a given set.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_not_be_in_set",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "value_set": {
            "title": "Value Set",
            "description": "A comma separated set of values. Remove all unnecessary whitespace.",
            "type": "array",
            "items": {}
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "value_set"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToBeBetween",
    "description": "Expect column entries to be between a minimum value and a maximum value.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum value for a column entry. If min_value is None, then max_value is treated as an upper bound, and there is no minimum value checked.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum value for a column entry. If max_value is None, then min_value is treated as a lower bound, and there is no maximum value checked.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, values must be strictly larger than min_value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, values must be strictly smaller than max_value",
            "default": false,
            "type": "boolean"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValueLengthsToBeBetween",
    "description": "Expect column entries to be strings with length between a minimum value and a maximum value.\nThis expectation only works for string-type values.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_value_lengths_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum value for a column entry length. If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has no minimum.",
            "default": false,
            "type": "integer"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum value for a column entry length. If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has no maximum.",
            "default": false,
            "type": "integer"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValueLengthsToEqual",
    "description": "Expect column entries to be strings with length equal to the provided value.\nThis expectation only works for string-type values.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_value_lengths_to_equal",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "value": {
            "title": "Value",
            "description": "The expected value for a column entry length.",
            "type": "integer"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToMatchRegex",
    "description": "Expect column entries to be strings that match a given regular expression.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_match_regex",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "regex": {
            "title": "Regex",
            "description": "The regular expression the column entries should match. Valid matches can be found anywhere in the string, for example “[at]+” will identify the following strings as expected: “cat”, “hat”, “aa”, “a”, and “t”, and the following strings as unexpected: “fish”, “dog”.",
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "regex"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToNotMatchRegex",
    "description": "Expect column entries to be strings that do NOT match a given regular expression. The regex must NOT match any portion of the provided string. .",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_not_match_regex",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "regex": {
            "title": "Regex",
            "description": "The regular expression the column entries should NOT match. For example, “[at]+” would identify the following strings as expected: “fish”, “dog”, and the following as unexpected: “cat”, “hat”",
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "regex"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToMatchRegexList",
    "description": "Expect the column entries to be strings that can be matched to either any of or all of a list of regular expressions. Matches can be anywhere in the string.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_match_regex_list",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "regex_list": {
            "title": "Regex List",
            "description": "The list of regular expressions which the column entries should match.",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "match_on": {
            "title": "Match On",
            "description": "“any” or “all”. Use “any” if the value should match at least one regular expression in the list. Use “all” if it should match each regular expression in the list.",
            "enum": [
              "any",
              "all"
            ],
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "regex_list",
          "match_on"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnValuesToNotMatchRegexList",
    "description": "Expect the column entries to be strings that do not match any of a list of regular expressions. Matches can be anywhere in the string.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_values_to_not_match_regex_list",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "regex_list": {
            "title": "Regex List",
            "description": "The list of regular expressions which the column entries should match.",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "match_on": {
            "title": "Match On",
            "description": "“any” or “all”. Use “any” if the value should match at least one regular expression in the list. Use “all” if it should match each regular expression in the list.",
            "enum": [
              "any",
              "all"
            ],
            "type": "string"
          },
          "mostly": {
            "title": "Mostly",
            "description": "A float between 0 and 1. When an expectations result is higher that this value, it will be marked as a successful run.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "regex_list",
          "match_on"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnMeanToBeBetween",
    "description": "Expect the column mean to be between a minimum value and a maximum value (inclusive).\nmin_value and max_value are both inclusive unless strict_min or strict_max are set to True.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_mean_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum value for the column mean. If min_value is None, then max_value is treated as an upper bound.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum value for the column mean. If max_value is None, then min_value is treated as a lower bound.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the column median must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the column median must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnMedianToBeBetween",
    "description": "Expect the column median to be between a minimum value and a maximum value.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_median_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum value for the column median. If min_value is None, then max_value is treated as an upper bound.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum value for the column median. If max_value is None, then min_value is treated as a lower bound.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the column median must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the column median must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnUniqueValueCountToBeBetween",
    "description": "Expect the number of unique values to be between a minimum value and a maximum value. (inclusive)",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_unique_value_count_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum number of unique values allowed. If min_value is None, then max_value is treated as an upper bound",
            "type": "integer"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum number of unique values allowed. If max_value is None, then min_value is treated as a lower bound",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnProportionOfUniqueValuesToBeBetween",
    "description": "Expect the proportion of unique values to be between a minimum value and a maximum value.\nFor example, in a column containing [1, 2, 2, 3, 3, 3, 4, 4, 4, 4], there are 4 unique values and 10 total values for a proportion of 0.4.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_proportion_of_unique_values_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimum proportion of unique values. If min_value is None, then max_value is treated as an upper bound.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximum proportion of unique values. If max_value is None, then min_value is treated as a lower bound.",
            "minimum": 0,
            "maximum": 1,
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the minimum proportion of unique values must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the maximum proportion of unique values must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnSumToBeBetween",
    "description": "Expect the column to sum to be between an min and max value",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_sum_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimal sum allowed.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximal sum allowed.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the minimal sum must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the maximal sum must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectMultiColumnSumToEqual",
    "description": "Expect the sum of row values is the same for each row, summing only values in column_list, and equal to sum_total.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_multicolumn_sum_to_equal",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_list": {
            "title": "Column List",
            "description": "The column names, in the correct order.",
            "form_type": "multi_column_select",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "sum_total": {
            "title": "Sum Total",
            "type": "integer"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_list",
          "sum_total"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnMinToBeBetween",
    "description": "Expect the column minimum to be between an min and max value",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_min_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimal column minimum allowed.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximal column minimum allowed.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the minimal column minimum must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the maximal column minimum must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "parse_strings_as_datetimes": {
            "title": "Parse Strings As Datetimes",
            "description": "If True, parse min_value, max_values, and all non-null column values to datetimes before making comparisons.",
            "default": false,
            "type": "boolean"
          },
          "output_strftime_format": {
            "title": "Output Strftime Format",
            "description": "A valid strfime format for datetime output. Only used if parse_strings_as_datetimes=True.",
            "type": "string"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnMaxToBeBetween",
    "description": "Expect the column maximum to be between an min and max value",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_max_to_be_between",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column": {
            "title": "Column",
            "description": "The column to be analyzed.",
            "form_type": "column_select",
            "type": "string"
          },
          "min_value": {
            "title": "Min Value",
            "description": "The minimal column minimum allowed.",
            "type": "number"
          },
          "max_value": {
            "title": "Max Value",
            "description": "The maximal column minimum allowed.",
            "type": "number"
          },
          "strict_min": {
            "title": "Strict Min",
            "description": "If True, the minimal column minimum must be strictly larger than min value.",
            "default": false,
            "type": "boolean"
          },
          "strict_max": {
            "title": "Strict Max",
            "description": "If True, the maximal column minimum must be strictly smaller than max value.",
            "default": false,
            "type": "boolean"
          },
          "parse_strings_as_datetimes": {
            "title": "Parse Strings As Datetimes",
            "description": "If True, parse min_value, max_values, and all non-null column values to datetimes before making comparisons.",
            "default": false,
            "type": "boolean"
          },
          "output_strftime_format": {
            "title": "Output Strftime Format",
            "description": "A valid strfime format for datetime output. Only used if parse_strings_as_datetimes=True.",
            "type": "string"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column",
          "min_value",
          "max_value"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_aggregate_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  },
  {
    "title": "ExpectColumnPairValuesToBeEqual",
    "description": "Expect the values in column A to be the same as column B.",
    "type": "object",
    "properties": {
      "dataset_id": {
        "title": "Dataset Id",
        "type": "string"
      },
      "datasource_id": {
        "title": "Datasource Id",
        "type": "string"
      },
      "expectation_type": {
        "title": "Expectation Type",
        "default": "expect_column_pair_values_to_be_equal",
        "type": "string"
      },
      "kwargs": {
        "title": "Kwargs",
        "type": "object",
        "properties": {
          "column_A": {
            "title": "Column A",
            "description": "The first column name.",
            "form_type": "column_select",
            "type": "string"
          },
          "column_B": {
            "title": "Column B",
            "description": "The second column name.",
            "form_type": "column_select",
            "type": "string"
          },
          "ignore_row_if": {
            "title": "Ignore Row If",
            "description": "Ignore row if.",
            "enum": [
              "both_values_are_missing",
              "either_value_is_missing",
              "neither"
            ],
            "type": "string"
          },
          "result_format": {
            "title": "Result Format",
            "default": "SUMMARY",
            "type": "string"
          },
          "include_config": {
            "title": "Include Config",
            "default": true,
            "type": "boolean"
          },
          "catch_exceptions": {
            "title": "Catch Exceptions",
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "column_A",
          "column_B",
          "ignore_row_if"
        ],
        "additionalProperties": false
      },
      "meta": {
        "title": "Meta",
        "type": "object"
      },
      "result_type": {
        "title": "Result Type",
        "default": "column_map_expectation",
        "type": "string"
      },
      "create_date": {
        "title": "Create Date",
        "type": "string"
      },
      "modified_date": {
        "title": "Modified Date",
        "type": "string"
      }
    },
    "required": [
      "dataset_id",
      "datasource_id",
      "kwargs"
    ],
    "additionalProperties": false
  }
];
