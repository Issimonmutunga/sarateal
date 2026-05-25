from datetime import date

from app.data_sources.weather.open_meteo import (
    DailyWeatherRecord,
    build_open_meteo_forecast_params,
    parse_open_meteo_daily_forecast,
)


def test_build_open_meteo_forecast_params():
    params = build_open_meteo_forecast_params(
        latitude=-1.286389,
        longitude=36.817223,
        forecast_days=3,
    )

    assert params["latitude"] == -1.286389
    assert params["longitude"] == 36.817223
    assert params["forecast_days"] == 3
    assert params["timezone"] == "auto"
    assert "temperature_2m_max" in params["daily"]
    assert "temperature_2m_min" in params["daily"]
    assert "precipitation_sum" in params["daily"]


def test_parse_open_meteo_daily_forecast():
    payload = {
        "latitude": -1.286389,
        "longitude": 36.817223,
        "daily": {
            "time": [
                "2026-05-25",
                "2026-05-26",
            ],
            "temperature_2m_max": [
                26.5,
                27.0,
            ],
            "temperature_2m_min": [
                14.2,
                15.1,
            ],
            "precipitation_sum": [
                2.4,
                0.0,
            ],
        },
    }

    records = parse_open_meteo_daily_forecast(payload)

    assert len(records) == 2
    assert records[0] == DailyWeatherRecord(
        latitude=-1.286389,
        longitude=36.817223,
        forecast_date=date(2026, 5, 25),
        max_temperature_c=26.5,
        min_temperature_c=14.2,
        precipitation_mm=2.4,
    )
    assert records[1].forecast_date == date(2026, 5, 26)
    assert records[1].precipitation_mm == 0.0


def test_parse_open_meteo_daily_forecast_handles_missing_daily_values():
    payload = {
        "latitude": -1.286389,
        "longitude": 36.817223,
        "daily": {
            "time": [
                "2026-05-25",
            ],
            "temperature_2m_max": [],
            "temperature_2m_min": [],
            "precipitation_sum": [],
        },
    }

    records = parse_open_meteo_daily_forecast(payload)

    assert len(records) == 1
    assert records[0].max_temperature_c is None
    assert records[0].min_temperature_c is None
    assert records[0].precipitation_mm is None