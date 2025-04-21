# 🧠 MCP Server Practice

A modular FastAPI-based server powered by **FastMCP**, showcasing practical implementations of AI tools, math operations, web search, audio response generation, and external API integration.

---

## 🚀 Core Functionalities

### 🔧 Math Utilities
- `add(a, b)`: Returns the sum of two integers.
- `multiply(a, b)`: Returns the product of two integers.

### 🌤️ Weather API Integration
- `get_weather(city)`: Fetches live weather data for a specified city using the [WeatherAPI](https://www.weatherapi.com/).

### 🌐 Web Search (via OpenAI Tools)
- `web_search(query)`: Performs a live web search using OpenAI’s web search tool and returns a concise result.

### 🔊 Audio Response Generation
- `audio_query(text)`: Converts a text query into spoken audio (WAV format) using OpenAI’s `gpt-4o` audio capabilities. Audio files are saved automatically to the `/audio` folder.

### 🙋‍♂️ Custom Resource Example
- `greeting://{name}`: Returns a personalized greeting string using the resource-based route.

---

## 🛠️ Built With

- **FastMCP**: A server interface for tool-based workflows.
- **FastAPI**: Web framework for high-performance APIs.
- **OpenAI**: Powering AI-based search, chat, and audio generation.
- **WeatherAPI**: External API for real-time weather updates.
- **Python + dotenv**: For scripting and secure environment variable handling.

---

## 💻 How It Works

Each tool is defined using the `@mcp.tool()` decorator, making it accessible as a callable interface for AI agents or CLI tools. The server runs with:

```bash
mcp.run(transport="stdio")
