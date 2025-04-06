from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """Add two numbers"""
    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

@mcp.tool()
def get_weather(city):
    """Fetch current weather data for a given city using the Weather API"""
    
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "API key not found in environment"}

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}

    data = response.json()

    weather_info = {
        "city": data["location"]["name"],
        "temperature_celsius": data["current"]["temp_c"],
        "temperature_fahrenheit": data["current"]["temp_f"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "wind_kph": data["current"]["wind_kph"]
    }

    return weather_info

if __name__=="__main__":
    mcp.run(transport="stdio")

