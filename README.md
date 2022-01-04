# python-eloverblik [![Test](https://github.com/SimonLarsen/energinet-eloverblik/actions/workflows/test.yml/badge.svg)](https://github.com/SimonLarsen/energinet-eloverblik/actions/workflows/test.yml) ![MIT License](https://img.shields.io/badge/license-MIT%20License-blue.svg)

A Python wrapper for the Eloverblik.dk API.

## Installation

Make sure [setuptools](https://github.com/pypa/setuptools) is installed.
Clone the repository and navigate to the root of the project.
Install the package using pip:

```bash
pip install .
```

## Usage

```python
from eloverblik import CustomerAPI
from datetime import datetime, timedelta

REFRESH_TOKEN = "..."
api = CustomerAPI(REFRESH_TOKEN)

meters = api.get_metering_points()
meter_id = meters[0]["meteringPointId"]

data = api.get_time_series(
    [meter_id],
    datetime.now()-timedelta(days=28),
    datetime.now(),
    "hour"
)

df = data[0].series[0].to_pandas()
```
