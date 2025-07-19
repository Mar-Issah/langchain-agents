from langchain_core.tools import tool


# 	TOOLS FOR BASIC CALCULATOR BELOW
@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' and 'y'."""
    return x * y


@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the power of 'y'."""
    return x**y


@tool
def subtract(x: float, y: float) -> float:
    """Subtract 'x' from 'y'."""
    return y - x


@tool
def divide(x: float, y: float) -> float:
    """Divide 'y' by 'x'."""
    if x == 0:
        raise ValueError("Cannot divide by zero.")
    return y / x


# END OF TOOLS FOR BASIC CALCULATOR BELOW


# TOOLS FOR WEATHER INFORMATION BELOW
import requests
from datetime import datetime


@tool
def get_location_from_ip() -> str:
    """Get the geographical location based on the IP address."""
    try:
        response = requests.get("https://ipinfo.io/json")
        # Get the IP address information in JSON format below
        data = response.json()
        if "loc" in data:
            latitude, longitude = data["loc"].split(",")
            data = (
                f"Latitude: {latitude},\n"
                f"Longitude: {longitude},\n"
                f"City: {data.get('city', 'N/A')},\n"
                f"Country: {data.get('country', 'N/A')}"
            )
            return data
        else:
            return "Location could not be determined."
    except Exception as e:
        return f"Error occurred: {e}"


@tool
def get_current_datetime() -> str:
    """Return the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# TOOLS FOR WEATHER INFORMATION BELOW
