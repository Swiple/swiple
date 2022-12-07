from typing import Annotated, Union, Literal, List
from pydantic.fields import Field
from app.models.base_model import BaseModel


class SampleUsingLimitParameters(BaseModel):
    n: int = Field(title="Number of rows", gt=0, description="Number of rows")


class SampleUsingLimit(BaseModel):
    """
    First n rows of batch
    """
    class Config:
        title = "Sample using limit"
    sampling_method: Literal["sample_using_limit"]
    sampling_kwargs: SampleUsingLimitParameters


class SampleUsingRandomParameters(BaseModel):
    p: float = Field(title="Fraction of rows", gt=0, le=1, placeholder=0.8, description="Fraction of total rows")


class SampleUsingRandom(BaseModel):
    """
    Rows selected at random, whose number amounts to selected fraction of total number of rows in batch
    """
    class Config:
        title = "Sample using random"
    sampling_method: Literal["sample_using_random"]
    sampling_kwargs: SampleUsingRandomParameters


class SampleUsingModParameters(BaseModel):
    column_name: str = Field(form_type="column_select", placeholder="Column Name of type <int>")
    mod: int = Field(title="mod", gt=0, description="The nth row to include in sample")
    value: int = Field()


class SampleUsingMod(BaseModel):
    """
    Take the mod of named column, and only keep rows that match the given value.
    e.g. If row 1 of column x has a value of 5 and you have set 'mod' to 4 and 'value' to 1,
    row 1 would be included in your dataset.
    """
    class Config:
        title = "Sample using mod"
    sampling_method: Literal["sample_using_mod"]
    sampling_kwargs: SampleUsingModParameters


class SampleUsingAListParameters(BaseModel):
    column_name: str = Field(form_type="column_select")
    value_list: List[str] = Field(description="")


class SampleUsingAList(BaseModel):
    """
    Match the values in the named column against value_list, and only keep the matches
    """
    class Config:
        title = "Sample using a list"
    sampling_method: Literal["sample_using_a_list"]
    sampling_kwargs: SampleUsingAListParameters


class SampleUsingHashParameters(BaseModel):
    column_name: str = Field(form_type="column_select")
    hash_digits: int = Field(gt=0, description="")
    hash_value: str = Field(description="")


class SampleUsingHash(BaseModel):
    """
    Hash the values in the named column (using "md5" hash function), and only keep rows that match the given hash_value
    """
    class Config:
        title = "Sample using hash"
    sampling_method: Literal["sample_using_hash"]
    sampling_kwargs: SampleUsingModParameters


Sampling = Annotated[Union[
    SampleUsingLimit,
    SampleUsingRandom,
    SampleUsingMod,
    SampleUsingAList,
    SampleUsingHash,
], Field(discriminator="sampling_method")]
