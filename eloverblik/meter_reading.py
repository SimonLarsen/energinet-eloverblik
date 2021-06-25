from typing import Dict, Any
from datetime import datetime
import pandas as pd


DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"


class MeterReading:
    def __init__(self, data: Dict[str, Any]):
        self.id = data["meteringPointId"]
        self.data = []
        for reading in data["readings"]:
            row = dict(
                read=datetime.strptime(
                    reading["readingDate"], DATETIME_FORMAT
                ),
                registered=datetime.strptime(
                    reading["registrationDate"], DATETIME_FORMAT
                ),
                meterNumber=reading["meterNumber"],
                reading=float(reading["meterReading"]),
                unit=reading["measurementUnit"],
            )
            self.data.append(row)

    def to_pandas(self) -> pd.DataFrame:
        """Get readings as Pandas data frame."""
        return pd.DataFrame(self.data)
