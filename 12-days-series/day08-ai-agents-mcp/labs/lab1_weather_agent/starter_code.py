"""
Lab 1: Weather Agent - Starter Code

Objective: Create an agent that can fetch weather information using MCP.
"""

from typing import Dict, Any
from datetime import datetime

class WeatherTool:
    """Weather information tool"""
    
    def __init__(self):
        self.name = "get_weather"
        self.description = "Get weather information for a city"
        self.weather_data = {
            "london": {"temp_c": 15, "condition": "Cloudy", "humidity": 72},
            "tokyo": {"temp_c": 22, "condition": "Sunny", "humidity": 60},
            "new york": {"temp_c": 18, "condition": "Rainy", "humidity": 80},
            "paris": {"temp_c": 16, "condition": "Partly Cloudy", "humidity": 65},
            "sydney": {"temp_c": 25, "condition": "Sunny", "humidity": 55},
        }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "city": {"type": "string", "description": "City name"},
                "units": {"type": "string", "description": "Temperature units", "default": "celsius"}
            }
        }
    
    def celsius_to_fahrenheit(self, temp_c: float) -> float:
        return temp_c * 9/5 + 32
    
    def execute(self, city: str, units: str = "celsius") -> Dict[str, Any]:
        city_lower = city.lower()
        weather = self.weather_data.get(city_lower, {"temp_c": 20, "condition": "Unknown", "humidity": 50})
        
        temp = weather["temp_c"]
        if units.lower() == "fahrenheit":
            temp = self.celsius_to_fahrenheit(temp)
            unit_symbol = "F"
        else:
            unit_symbol = "C"
        
        return {
            "success": True,
            "city": city,
            "temperature": f"{temp}{unit_symbol}",
            "condition": weather["condition"],
            "humidity": f"{weather['humidity']}%",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print("Testing Weather Tool\n")
    tool = WeatherTool()
    for city in ["London", "Tokyo", "New York", "Dubai"]:
        result = tool.execute(city, units="celsius")
        print(f"{city}: {result['temperature']}, {result['condition']}")
