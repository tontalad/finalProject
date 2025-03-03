from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Literal

class QueryParams(BaseModel):
    filter_query: Optional[Dict[str, str]] = Field(
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

    projection: Optional[Dict] = Field(
        default=None,
        description="A dictionary for projection (e.g., {'name': 1, '_id': 0})."
    )

    @field_validator("sort")
    def validate_sort(cls, value):
        if value:
            for field, order in value.items():
                if order not in ["asc", "desc"]:
                    raise ValueError("Sort order must be 'asc' or 'desc'.")
        return value  