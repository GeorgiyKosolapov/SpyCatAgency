import httpx
from functools import lru_cache

THE_CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


@lru_cache(maxsize=1)
def get_valid_breeds() -> set:
    try:
        response = httpx.get(THE_CAT_API_URL, timeout=10.0)
        response.raise_for_status()
        breeds_data = response.json()
        return {breed["name"].lower() for breed in breeds_data}
    except Exception:
        return set()


def validate_breed(breed: str) -> bool:
    valid_breeds = get_valid_breeds()
    return breed.lower() in valid_breeds


def clear_breed_cache():
    get_valid_breeds.cache_clear()

