from dataclasses import dataclass


@dataclass(frozen=True)
class CountyCoordinate:
    county: str
    latitude: float
    longitude: float
    location_type: str = "county"


# Published geographic coordinates of each county's gazetted headquarters
# town (Government of Kenya administrative data / publicly available atlas
# records). Reference data only — never simulated observations.
KENYA_COUNTY_COORDINATES: list[CountyCoordinate] = [
    CountyCoordinate(county="Baringo", latitude=0.4916, longitude=35.7426),
    CountyCoordinate(county="Bomet", latitude=-0.7833, longitude=35.3500),
    CountyCoordinate(county="Bungoma", latitude=0.5635, longitude=34.5606),
    CountyCoordinate(county="Busia", latitude=0.4601, longitude=34.1112),
    CountyCoordinate(county="Elgeyo-Marakwet", latitude=0.6697, longitude=35.5082),
    CountyCoordinate(county="Embu", latitude=-0.5365, longitude=37.4589),
    CountyCoordinate(county="Garissa", latitude=-0.4532, longitude=39.6461),
    CountyCoordinate(county="Homa Bay", latitude=-0.5273, longitude=34.4571),
    CountyCoordinate(county="Isiolo", latitude=0.3547, longitude=37.5822),
    CountyCoordinate(county="Kajiado", latitude=-2.0780, longitude=36.7810),
    CountyCoordinate(county="Kakamega", latitude=0.2827, longitude=34.7519),
    CountyCoordinate(county="Kericho", latitude=-0.3692, longitude=35.2830),
    CountyCoordinate(county="Kiambu", latitude=-1.1714, longitude=36.8298),
    CountyCoordinate(county="Kilifi", latitude=-3.6305, longitude=39.8499),
    CountyCoordinate(county="Kirinyaga", latitude=-0.4989, longitude=37.2803),
    CountyCoordinate(county="Kisii", latitude=-0.6819, longitude=34.7665),
    CountyCoordinate(county="Kisumu", latitude=-0.0917, longitude=34.7680),
    CountyCoordinate(county="Kitui", latitude=-1.3748, longitude=38.0106),
    CountyCoordinate(county="Kwale", latitude=-4.1737, longitude=39.4525),
    CountyCoordinate(county="Laikipia", latitude=0.0066, longitude=37.0725),
    CountyCoordinate(county="Lamu", latitude=-2.2713, longitude=40.9022),
    CountyCoordinate(county="Machakos", latitude=-1.5177, longitude=37.2634),
    CountyCoordinate(county="Makueni", latitude=-1.7856, longitude=37.6265),
    CountyCoordinate(county="Mandera", latitude=3.9366, longitude=41.8670),
    CountyCoordinate(county="Marsabit", latitude=2.3340, longitude=37.9906),
    CountyCoordinate(county="Meru", latitude=0.0463, longitude=37.6559),
    CountyCoordinate(county="Migori", latitude=-1.0667, longitude=34.4787),
    CountyCoordinate(county="Mombasa", latitude=-4.0435, longitude=39.6682),
    CountyCoordinate(county="Murang'a", latitude=-0.7500, longitude=37.1500),
    CountyCoordinate(county="Nairobi", latitude=-1.286389, longitude=36.817223),
    CountyCoordinate(county="Nakuru", latitude=-0.3031, longitude=36.0800),
    CountyCoordinate(county="Nandi", latitude=0.2039, longitude=35.1050),
    CountyCoordinate(county="Narok", latitude=-1.0833, longitude=36.0000),
    CountyCoordinate(county="Nyamira", latitude=-0.5614, longitude=34.9805),
    CountyCoordinate(county="Nyandarua", latitude=-0.2710, longitude=36.3794),
    CountyCoordinate(county="Nyeri", latitude=-0.4167, longitude=36.9500),
    CountyCoordinate(county="Samburu", latitude=1.0960, longitude=36.6980),
    CountyCoordinate(county="Siaya", latitude=0.0607, longitude=34.2857),
    CountyCoordinate(county="Taita-Taveta", latitude=-3.3894, longitude=38.5562),
    CountyCoordinate(county="Tana River", latitude=-1.4833, longitude=40.0333),
    CountyCoordinate(county="Tharaka-Nithi", latitude=-0.3333, longitude=37.6422),
    CountyCoordinate(county="Trans Nzoia", latitude=1.0157, longitude=35.0062),
    CountyCoordinate(county="Turkana", latitude=3.1167, longitude=35.5967),
    CountyCoordinate(county="Uasin Gishu", latitude=0.5143, longitude=35.2698),
    CountyCoordinate(county="Vihiga", latitude=0.0697, longitude=34.7267),
    CountyCoordinate(county="Wajir", latitude=1.7471, longitude=40.0573),
    CountyCoordinate(county="West Pokot", latitude=1.2392, longitude=35.1116),
]


def list_county_coordinates() -> list[CountyCoordinate]:
    return KENYA_COUNTY_COORDINATES


def find_county_coordinate(county: str) -> CountyCoordinate | None:
    normalized_county = county.strip().lower()

    for coordinate in KENYA_COUNTY_COORDINATES:
        if coordinate.county.lower() == normalized_county:
            return coordinate

    return None