import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Union
from eloverblik.time_series import TimeSeries
from eloverblik.aggregation import Aggregation
from eloverblik.meter_reading import MeterReading


API_URL_PROD = "https://api.eloverblik.dk/CustomerApi"
API_URL_PREPROD = "https://apipreprod.eloverblik.dk/CustomerApi"
ACCESS_TOKEN_VALID_TIME = timedelta(minutes=59)


class CustomerAPI:
    def __init__(self, refresh_token: str, preprod: bool = False) -> None:
        self._refresh_token = refresh_token
        self._access_token = ""
        self._access_token_time = datetime.fromtimestamp(0)
        self._api_url = API_URL_PREPROD if preprod else API_URL_PROD

    def _get_access_token(self) -> str:
        if datetime.now() - self._access_token_time > ACCESS_TOKEN_VALID_TIME:
            response = requests.get(
                f"{self._api_url}/api/1/token",
                headers={"Authorization": f"Bearer {self._refresh_token}"},
            )
            response.raise_for_status()
            js = response.json()
            self._access_token = js["result"]
            self._access_token_time = datetime.now()

        return self._access_token

    def _get(
        self, path: str, params: Dict[str, Any] = None
    ) -> requests.Response:
        """
        Make a GET request using data access token.

        Parameters
        ----------
        path : str
            API path string.
        params : dict
            Request parameters as key-value pairs.

        Returns
        -------
        requests.Response
            Response object.
        """
        if len(path) == 0:
            raise ValueError("API path can't be an empty string.")
        if path[0] != "/":
            path = "/" + path

        token = self._get_access_token()
        response = requests.get(
            f"{self._api_url}{path}",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response

    def _post(
        self,
        path: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
    ) -> requests.Response:
        """
        Make a POST request using data access token.

        Parameters
        ----------
        path : str
            API path string.
        data : dict
            Form-encoded parameters as key-value pairs.
        json: dict
            JSON parameter data. Using this parameter will change the
            ``Content-Type`` in the header to ``application/json``.

        Returns
        -------
        requests.Reponse
            Response object.
        """
        if len(path) == 0:
            raise ValueError("API path can't be an empty string.")
        if path[0] != "/":
            path = "/" + path

        token = self._get_access_token()
        response = requests.post(
            f"{self._api_url}{path}",
            data=data,
            json=json,
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response

    def get_metering_points(self, include_all: bool = False) -> Dict[str, Any]:
        """
        Get list of metering points.

        Parameters
        ----------
        include_all : bool
            When false, only metering points with relations are returned.

        Returns
        -------
        list of dictionaries
            Information for metering points.
        """
        response = self._get(
            "/api/1/meteringpoints/meteringpoints",
            params={"includeAll": include_all},
        )
        return response.json()["result"]

    def get_metering_point_details(
        self, point_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get details for a list of metering points.

        Parameters
        ----------
        point_ids : list of strings
            List of metering point IDs.

        Returns
        -------
        list of dictionaries
            List of dictionaries with metering point details.
        """
        if type(point_ids) != list:
            raise ValueError("point_ids must be a list.")

        params = {"meteringPoints": {"meteringPoint": point_ids}}
        response = self._post(
            "/api/1/meteringpoints/meteringpoint/getdetails",
            json=params,
        )
        return [e["result"] for e in response.json()["result"]]

    def get_metering_point_charges(
        self, point_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get price data for a list of metering points.

        Parameters
        ----------
        point_ids : list of strings

        Returns
        -------
        list of dictionaries
            List of dictionaries with price data.
        """
        if type(point_ids) != list:
            raise ValueError("point_ids must be a list.")

        params = {"meteringPoints": {"meteringPoint": point_ids}}
        response = self._post(
            "/api/1/meteringpoints/meteringpoint/getcharges",
            json=params,
        )
        return [e["result"] for e in response.json()["result"]]

    def get_time_series(
        self,
        point_ids: List[str],
        start: datetime,
        end: datetime,
        aggregation: Union[Aggregation, str],
    ) -> List[TimeSeries]:
        """
        Get time series for a list of metering points.

        Parameters
        ----------
        point_ids : list of strings
            List of metering point IDs.
        start : datetime
            Series period start.
        end : datetime
            Series period end.
        aggregation : eloverblik.Aggregation or str
            Data aggregation resolution.

        Returns
        -------
        list of TimeSeries objects
            A list of TimeSeries objects for each metering point.
        """
        if type(point_ids) != list:
            raise ValueError("point_ids must be a list.")

        if type(aggregation) == str:
            if aggregation.upper() not in Aggregation.__members__.keys():
                raise ValueError(f"Invalid aggregation value '{aggregation}'.")
            aggregation = Aggregation[aggregation.upper()]
        elif type(aggregation) != Aggregation:
            raise ValueError(
                "Aggregation must be of type 'str' or 'Aggregation'."
            )

        urlStart = start.strftime("%Y-%m-%d")
        urlEnd = end.strftime("%Y-%m-%d")
        urlAgg = aggregation.value
        params = {"meteringPoints": {"meteringPoint": point_ids}}
        response = self._post(
            f"/api/1/meterdata/gettimeseries/{urlStart}/{urlEnd}/{urlAgg}",
            json=params,
        )
        return [
            TimeSeries(res["MyEnergyData_MarketDocument"])
            for res in response.json()["result"]
        ]

    def get_meter_readings(
        self,
        point_ids: List[str],
        start: datetime,
        end: datetime,
    ) -> Any:
        """
        Get meter readings for a list of metering points.

        Parameters
        ----------
        point_ids : list of strings
            List of metering point IDs.
        start : datetime
            Series period start.
        end : datetime
            Series period end.

        Returns
        -------
        list of MeterReading objects
            A list of MeterReading objects for eact metering point.
        """
        if type(point_ids) != list:
            raise ValueError("point_ids must be a list.")

        params = {"meteringPoints": {"meteringPoint": point_ids}}
        urlStart = start.strftime("%Y-%m-%d")
        urlEnd = end.strftime("%Y-%m-%d")
        response = self._post(
            f"/api/1/meterdata/getmeterreadings/{urlStart}/{urlEnd}",
            json=params,
        )
        return [
            MeterReading(res["result"]) for res in response.json()["result"]
        ]
