from datetime import date

from app.data_sources.weather import DailyWeatherRecord
from app.services.weather_signals import (
    build_weather_risk_signal,
    build_weather_risk_signals,
    classify_heat_risk,
    classify_rainfall_signal,
    summarize_weather_signal,
)


def test_classify_heat_risk():
    assert classify_heat_risk(None) == "unknown"
    assert classify_heat_risk(36) == "high"
    assert classify_heat_risk(32) == "medium"
    assert classify_heat_risk(25) == "low"


def test_classify_rainfall_signal():
    assert classify_rainfall_signal(None) == "unknown"
    assert classify_rainfall_signal(55) == "heavy_rain"
    assert classify_rainfall_signal(15) == "moderate_rain"
    assert classify_rainfall_signal(2) == "light_rain"
    assert classify_rainfall_signal(0) == "dry"


def test_summarize_weather_signal_prioritizes_high_heat_and_dry_conditions():
    summary = summarize_weather_signal(
        heat_risk="high",
        rainfall_signal="dry",
    )

    assert "High heat" in summary
    assert "supply risk" in summary


def test_build_weather_risk_signal_from_daily_weather_record():
    record = DailyWeatherRecord(
        latitude=-1.286389,
        longitude=36.817223,
        forecast_date=date(2026, 5, 25),
        max_temperature_c=36,
        min_temperature_c=18,
        precipitation_mm=0,
    )

    signal = build_weather_risk_signal(record)

    assert signal.latitude == -1.286389
    assert signal.longitude == 36.817223
    assert signal.signal_date == date(2026, 5, 25)
    assert signal.heat_risk == "high"
    assert signal.rainfall_signal == "dry"
    assert signal.source_name == "Open-Meteo"


def test_build_weather_risk_signals_from_multiple_records():
    records = [
        DailyWeatherRecord(
            latitude=-1.286389,
            longitude=36.817223,
            forecast_date=date(2026, 5, 25),
            max_temperature_c=36,
            min_temperature_c=18,
            precipitation_mm=0,
        ),
        DailyWeatherRecord(
            latitude=-1.286389,
            longitude=36.817223,
            forecast_date=date(2026, 5, 26),
            max_temperature_c=27,
            min_temperature_c=16,
            precipitation_mm=60,
        ),
    ]

    signals = build_weather_risk_signals(records)

    assert len(signals) == 2
    assert signals[0].heat_risk == "high"
    assert signals[1].rainfall_signal == "heavy_rain"