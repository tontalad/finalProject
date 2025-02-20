from pydantic import BaseModel, Field, field_validator
from bson import Timestamp
from datetime import datetime
from typing import Optional, Dict, Literal

class QueryParams(BaseModel):
    filter_query: Optional[Dict] = Field(
        default=None,
        description="A dictionary for filtering (e.g., {'name': 'Math'})."
    )
    sort: Optional[Dict[str, Literal["asc", "desc"]]] = Field(
        default=None,
        description="A dictionary for sorting (e.g., {'name': 'asc'})."
    )
    limit: Optional[int] = Field(
        default=None,
        description="The maximum number of documents to return."
    )
    skip: Optional[int] = Field(
        default=None,
        description="The number of documents to skip."
    )

    @field_validator("sort")
    def validate_sort(cls, value):
        if value:
            for field, order in value.items():
                if order not in ["asc", "desc"]:
                    raise ValueError("Sort order must be 'asc' or 'desc'.")
        return value

def convert_timestamp(value):
    if isinstance(value, Timestamp):  # If it's a MongoDB Timestamp, convert it
        return datetime.fromtimestamp(value.as_datetime().timestamp())
    if isinstance(value, str) and value.strip() == "":  # Handle empty string case
        return None
    return value