python-eloverblik
-----------------

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
from datetime import datetime

REFRESH_TOKEN = "..."
api = CustomerAPI(REFRESH_TOKEN)

my_meter_id = "123456789"
readings = api.get_meter_readings(
    [my_meter_id],
    datetime(2021, 1, 1),
    datetime.now()
)

df = readings.data[0].to_pandas()
```
