from dataclasses import dataclass
from datetime import date
from typing import Any

import requests


OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass(frozen=True)
class DailyWeatherRecord:
    latitude: float
    longitude: float
    forecast_date: date
    max_temperature_c: float | None
    min_temperature_c: float | None
    precipitation_mm: float | None
    source_name: str = "Open-Meteo"


def build_open_meteo_forecast_params(
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
) -> dict[str, Any]:
    return {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(
            [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
            ]
        ),
        "forecast_days": forecast_days,
        "timezone": "auto",
    }


def parse_open_meteo_daily_forecast(
    payload: dict[str, Any],
) -> list[DailyWeatherRecord]:
    latitude = float(payload["latitude"])
    longitude = float(payload["longitude"])

    daily = payload.get("daily", {})

    dates = daily.get("time", [])
    max_temperatures = daily.get("temperature_2m_max", [])
    min_temperatures = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])

    records = []

    for index, forecast_date in enumerate(dates):
        records.append(
            DailyWeatherRecord(
                latitude=latitude,
                longitude=longitude,
                forecast_date=date.fromisoformat(forecast_date),
                max_temperature_c=max_temperatures[index]
                if index < len(max_temperatures)
                else None,
                min_temperature_c=min_temperatures[index]
                if index < len(min_temperatures)
                else None,
                precipitation_mm=precipitation[index]
                if index < len(precipitation)
                else None,
            )
        )

    return records


def fetch_open_meteo_daily_forecast(
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
    timeout_seconds: int = 20,
) -> list[DailyWeatherRecord]:
    response = requests.get(
        OPEN_METEO_FORECAST_URL,
        params=build_open_meteo_forecast_params(
            latitude=latitude,
            longitude=longitude,
            forecast_days=forecast_days,
        ),
        timeout=timeout_seconds,
    )

    response.raise_for_status()

    return parse_open_meteo_daily_forecast(response.json())