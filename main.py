"""Smart City 360 - a beginner-friendly city simulator demo."""

from datetime import datetime
import streamlit as st


STARTING_STATS = {
    "population": 1_240_000,
    "traffic": 68,
    "energy": 72,
    "water": 86,
    "waste": 78,
    "air_quality": 42,
}

SECTIONS = [
    "Dashboard",
    "Traffic",
    "Energy",
    "Water",
    "Waste",
    "Environment",
    "Emergency",
]

SECTION_INFO = {
    "Traffic": (
        "Traffic congestion",
        "Congestion changes when traffic events are handled by the control center.",
    ),
    "Energy": (
        "Renewable energy share",
        "The Power Plant supplies clean energy to the fictional city grid.",
    ),
    "Water": (
        "Water service coverage",
        "This value represents the share of city neighborhoods with reliable water service.",
    ),
    "Waste": (
        "Waste recycling rate",
        "This value represents the share of collected city waste that is recycled.",
    ),
    "Environment": (
        "Air quality index",
        "A lower Air Quality Index (AQI) is better. Values in this demo are illustrative.",
    ),
}

TRAFFIC_EVENTS = {
    "Traffic Jam": {
        "congestion": 12,
        "aqi": 5,
        "response": "Adaptive traffic signals activated and alternate routes suggested.",
    },
    "Road Blocked": {
        "congestion": 18,
        "aqi": 7,
        "response": "Road diversion activated and emergency route monitoring started.",
    },
    "Heavy Traffic": {
        "congestion": 8,
        "aqi": 3,
        "response": "Traffic signal timing adjusted to improve vehicle flow.",
    },
    "Clear Road": {
        "congestion": -10,
        "aqi": -4,
        "response": "Traffic returned toward normal flow and signal timing was restored.",
    },
}

EMERGENCY_EVENTS = {
    "Fire": {
        "service": "Fire Station",
        "traffic": 6,
        "aqi": 8,
        "response": "Fire Station dispatched. Nearby traffic signals switched to emergency priority.",
    },
    "Medical Emergency": {
        "service": "Hospital + Ambulance",
        "traffic": 4,
        "aqi": 1,
        "response": "Ambulance dispatched and Hospital emergency unit placed on alert.",
    },
    "Major Accident": {
        "service": "Police + Ambulance",
        "traffic": 10,
        "aqi": 3,
        "response": "Police secured the accident zone and an ambulance was dispatched.",
    },
    "Flood Warning": {
        "service": "Emergency Operations Center",
        "traffic": 8,
        "aqi": 2,
        "response": "Flood response activated. Water monitoring and emergency route planning started.",
    },
}


def current_time():
    """Return the current local time for an Event Log entry."""
    return datetime.now().strftime("%H:%M:%S")


def add_event(message):
    """Put the newest event at the top of the Event Log."""
    st.session_state.event_log.insert(
        0,
        {"time": current_time(), "message": message},
    )
    st.session_state.event_log = st.session_state.event_log[:8]


def reset_simulation():
    """Restore the fictional city to its starting values."""
    st
