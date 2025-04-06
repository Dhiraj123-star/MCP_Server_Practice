from mcp.server.fastmcp import FastMCP
import requests
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv
load_dotenv()

# Create the audio folder if it doesn't exist
if not os.path.exists("audio"):
    os.makedirs("audio")


# Helper to get the next file name like result1.wav, result2.wav, etc.
def get_next_filename():
    existing_files = os.listdir("audio")
    count = 1
    while f"result{count}.wav" in existing_files:
        count += 1
    return f"result{count}.wav"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

@mcp.tool()
def web_search(query:str)->str:
    response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input=query
    )
    return response.output_text

@mcp.tool()
def audio_query(query: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    filename = get_next_filename()
    filepath = os.path.join("audio", filename)
    with open(filepath, "wb") as f:
        f.write(wav_bytes)

if __name__=="__main__":
    mcp.run(transport="stdio")

