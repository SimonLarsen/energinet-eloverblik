from datetime import datetime
import pandas as pd

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class Table:
    def __init__(self, series):
        self.mRID = series["mRID"]
        self.businessType = series["businessType"]
        self.curveType = series["curveType"]
        self.unit = series["measurement_Unit.name"]

        self.data = []
        for elem in series["Period"]:
            for point in elem["Point"]:
                row = dict(
                    start=datetime.strptime(
                        elem["timeInterval"]["start"], DATETIME_FORMAT
                    ),
                    end=datetime.strptime(
                        elem["timeInterval"]["end"], DATETIME_FORMAT
                    ),
                    resolution=elem["resolution"],
                    position=int(point["position"]),
                    quantity=float(point["out_Quantity.quantity"]),
                    quality=point["out_Quantity.quality"],
                )
                self.data.append(row)

    def to_pandas(self) -> pd.DataFrame:
        """Convert time series table to a Pandas data frame."""
        return pd.DataFrame(self.data)


class TimeSeries:
    def __init__(self, doc):
        self.mRID = doc["mRID"]
        self.created = datetime.strptime(
            doc["createdDateTime"], DATETIME_FORMAT
        )
        self.start = datetime.strptime(
            doc["period.timeInterval"]["start"], DATETIME_FORMAT
        )
        self.end = datetime.strptime(
            doc["period.timeInterval"]["end"], DATETIME_FORMAT
        )
        self.series = [Table(series) for series in doc["TimeSeries"]]
