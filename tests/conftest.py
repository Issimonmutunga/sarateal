import pytest

from app.services.stored_locations import clear_stored_locations


@pytest.fixture(autouse=True)
def _reset_in_memory_cache():
    clear_stored_locations()

    yield