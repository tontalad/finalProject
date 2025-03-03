from pydantic import BaseModel, Field, field_validator
from bson import Timestamp
from datetime import datetime
from typing import Optional, Dict, Literal



def convert_timestamp(value):
    if isinstance(value, Timestamp):  # If it's a MongoDB Timestamp, convert it
        return datetime.fromtimestamp(value.as_datetime().timestamp())
    if isinstance(value, str) and value.strip() == "":  # Handle empty string case
        return None
    return value