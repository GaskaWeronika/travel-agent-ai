import random
from typing import TypedDict, Literal

from langchain_core.tools import tool


class UserPreferences(TypedDict):
    interests: list[str]
    transport: Literal["plane", "train", "car"]
    budget: list[int]
    travel_days: int


DESTINATIONS_DB = {
    "Paris": {"interests": ["culture", "romance"], "price_range": (1000, 3000)},
    "Venice": {"interests": ["culture", "romance"], "price_range": (800, 2000)},
    "Canary Islands": {"interests": ["relaxation", "beach"], "price_range": (1000, 2500)},
    "Thailand": {"interests": ["adventure", "beach"], "price_range": (1200, 4000)},
    "New York": {"interests": ["culture", "shopping"], "price_range": (1500, 3500)},
    "Rome": {"interests": ["culture", "historical sites"], "price_range": (900, 2500)},
    "Barcelona": {"interests": ["culture", "cuisine"], "price_range": (1000, 3000)},
    "London": {"interests": ["culture", "shopping"], "price_range": (1200, 3500)},
    "Dubai": {"interests": ["luxury", "shopping"], "price_range": (2000, 5000)},
    "Cape Town": {"interests": ["adventure", "nature"], "price_range": (1500, 3500)},
    "Santorini": {"interests": ["romance", "beach"], "price_range": (1500, 4000)},
    "Prague": {"interests": ["culture", "romance"], "price_range": (700, 2000)},
    "Amsterdam": {"interests": ["culture", "entertainment"], "price_range": (900, 2500)},
    "Zanzibar": {"interests": ["beach", "adventure"], "price_range": (1200, 3500)},
    "Marrakesh": {"interests": ["culture", "adventure"], "price_range": (800, 2500)},
    "Bangkok": {"interests": ["adventure", "culture"], "price_range": (800, 2500)},
    "Seychelles": {"interests": ["beach", "relaxation"], "price_range": (2500, 6000)},
    "Maldives": {"interests": ["beach", "luxury"], "price_range": (3000, 7000)},
    "Vienna": {"interests": ["culture", "music"], "price_range": (900, 2500)},
    "Kuala Lumpur": {"interests": ["adventure", "culture"], "price_range": (900, 2500)},
    "Bali": {"interests": ["adventure", "beach"], "price_range": (1200, 3500)},
    "Hawaii": {"interests": ["beach", "adventure"], "price_range": (2500, 6000)},
    "Los Angeles": {"interests": ["culture", "shopping"], "price_range": (2000, 5000)},
    "Mexico": {"interests": ["adventure", "culture"], "price_range": (1000, 3000)},
    "Sydney": {"interests": ["adventure", "culture"], "price_range": (2000, 5000)},
    "Tokyo": {"interests": ["culture", "modernity"], "price_range": (1800, 4500)},
    "Lisbon": {"interests": ["culture", "beach"], "price_range": (800, 2500)},
    "Toronto": {"interests": ["culture", "shopping"], "price_range": (1500, 4000)},
    "Cabo Verde": {"interests": ["beach", "relaxation"], "price_range": (1500, 3500)},
    "Reykjavik": {"interests": ["adventure", "nature"], "price_range": (1500, 4000)},
    "Bordeaux": {"interests": ["culture", "wine"], "price_range": (1000, 2500)},
    "Buenos Aires": {"interests": ["culture", "tango"], "price_range": (1200, 3500)},
    "Sao Paulo": {"interests": ["culture", "shopping"], "price_range": (1500, 4000)},
    "Montenegro": {"interests": ["beach", "adventure"], "price_range": (1000, 2500)},
    "Vancouver": {"interests": ["adventure", "nature"], "price_range": (2000, 5000)},
    "Helsinki": {"interests": ["culture", "modernity"], "price_range": (1200, 3500)},
}


@tool
def recommend_destinations(user_prefs: UserPreferences) -> list[str]:
    """Recommends 2 destinations based on user interests."""
    matches = []
    for interest in user_prefs["interests"]:
        matches += [dest for dest, data in DESTINATIONS_DB.items() if interest in data["interests"]]
    matches = list(set(matches))
    return random.sample(matches, 2) if len(matches) >= 2 else matches


@tool
def suggest_transport(user_prefs: UserPreferences) -> str:
    """Suggests the preferred mode of transport."""
    return f"Suggested mode of transport: {user_prefs['transport']}."


@tool
def suggest_budget(user_prefs: UserPreferences) -> str:
    """Estimates the overall travel budget."""
    min_bud, max_bud = user_prefs["budget"]
    days = user_prefs["travel_days"]
    daily_estimate = (min_bud + max_bud) // 2 // max(1, days)
    return f"Estimated daily budget: approximately {daily_estimate} PLN per day."