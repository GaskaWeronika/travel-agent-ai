from typing import Literal, TypedDict

class UserPreferences(TypedDict):
    interests: list[str]                
    transport: Literal["plane", "train", "car", "bus"]
    budget: tuple[int, int]             
    travel_days: int                    
    start_location: str                 
