from enum import Enum


class Aggregation(Enum):
    """Time series aggregation resolutions."""

    ACTUAL = "Actual"
    HOUR = "Hour"
    DAY = "Day"
    MONTH = "Month"
    QUARTER = "Quarter"
    YEAR = "Year"
