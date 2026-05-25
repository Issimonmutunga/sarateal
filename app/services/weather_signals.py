from dataclasses import dataclass
from datetime import date

from app.data_sources.weather import DailyWeatherRecord


@dataclass(frozen=True)
class WeatherRiskSignal:
    latitude: float
    longitude: float
    signal_date: date
    heat_risk: str
    rainfall_signal: str
    summary: str
    source_name: str


def classify_heat_risk(max_temperature_c: float | None) -> str:
    if max_temperature_c is None:
        return "unknown"

    if max_temperature_c >= 35:
        return "high"

    if max_temperature_c >= 30:
        return "medium"

    return "low"


def classify_rainfall_signal(precipitation_mm: float | None) -> str:
    if precipitation_mm is None:
        return "unknown"

    if precipitation_mm >= 50:
        return "heavy_rain"

    if precipitation_mm >= 10:
        return "moderate_rain"

    if precipitation_mm > 0:
        return "light_rain"

    return "dry"


def summarize_weather_signal(
    heat_risk: str,
    rainfall_signal: str,
) -> str:
    if heat_risk == "high" and rainfall_signal == "dry":
        return "High heat and dry conditions may stress crops and increase supply risk."

    if rainfall_signal == "heavy_rain":
        return "Heavy rainfall may affect transport, harvesting, and produce movement."

    if heat_risk == "medium":
        return "Moderate heat risk may affect sensitive produce and storage quality."

    if rainfall_signal in {"moderate_rain", "light_rain"}:
        return "Rainfall is present and should be monitored for market and logistics effects."

    if heat_risk == "low" and rainfall_signal == "dry":
        return "No major weather risk signal detected from the available forecast."

    return "Weather signal is incomplete or uncertain."


def build_weather_risk_signal(record: DailyWeatherRecord) -> WeatherRiskSignal:
    heat_risk = classify_heat_risk(record.max_temperature_c)
    rainfall_signal = classify_rainfall_signal(record.precipitation_mm)

    return WeatherRiskSignal(
        latitude=record.latitude,
        longitude=record.longitude,
        signal_date=record.forecast_date,
        heat_risk=heat_risk,
        rainfall_signal=rainfall_signal,
        summary=summarize_weather_signal(
            heat_risk=heat_risk,
            rainfall_signal=rainfall_signal,
        ),
        source_name=record.source_name,
    )


def build_weather_risk_signals(
    records: list[DailyWeatherRecord],
) -> list[WeatherRiskSignal]:
    return [build_weather_risk_signal(record) for record in records]