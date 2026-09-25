"""Smart City 360 - a beginner-friendly city simulator demo."""

from datetime import datetime

import streamlit as st


# Starting values for our fictional Greenfield City
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
    st.session_state.city_stats = STARTING_STATS.copy()
    st.session_state.simulation_runs = 0
    st.session_state.simulation_started = False

    st.session_state.event_log = [
        {
            "time": current_time(),
            "message": "City data reset to the Version 3 starting values.",
        }
    ]


# Page settings
st.set_page_config(
    page_title="Smart City 360",
    page_icon="🏙️",
    layout="wide",
)


# Create the initial session data
if "city_stats" not in st.session_state:
    st.session_state.city_stats = STARTING_STATS.copy()
    st.session_state.simulation_runs = 0
    st.session_state.simulation_started = False

    st.session_state.event_log = [
        {
            "time": current_time(),
            "message": "Smart City 360 dashboard is ready.",
        },
        {
            "time": current_time(),
            "message": "North Park sensors are reporting normally.",
        },
        {
            "time": current_time(),
            "message": "Power Plant is connected to the city grid.",
        },
    ]


# Sidebar
st.sidebar.title("Smart City 360")
st.sidebar.caption("CITY OPERATIONS")

selected_section = st.sidebar.radio(
    "Navigate",
    SECTIONS,
)

st.sidebar.divider()

st.sidebar.caption("DEMO CITY")
st.sidebar.write("Greenfield")

if st.session_state.simulation_started:
    st.sidebar.success("Simulation active")
else:
    st.sidebar.info("Simulation ready")


# Main title
title_column, control_column = st.columns([3, 1])


with title_column:
    st.title("Smart City 360")
    st.caption("Interactive Smart City Simulator")
    st.write("Greenfield City · Live operations overview")


with control_column:
    st.write("### Simulation controls")

    start_column, reset_column = st.columns(2)

    with start_column:
        start_clicked = st.button(
            "Start Simulation",
            type="primary",
            use_container_width=True,
        )

    with reset_column:
        reset_clicked = st.button(
            "Reset",
            use_container_width=True,
        )


# Simulation controls
if start_clicked:
    stats = st.session_state.city_stats

    run_number = st.session_state.simulation_runs + 1

    stats["traffic"] = max(
        36,
        stats["traffic"] - 4,
    )

    stats["energy"] = min(
        94,
        stats["energy"] + 2,
    )

    stats["water"] = min(
        98,
        stats["water"] + 1,
    )

    stats["waste"] = min(
        94,
        stats["waste"] + 2,
    )

    stats["air_quality"] = max(
        20,
        stats["air_quality"] - 3,
    )

    st.session_state.simulation_runs = run_number
    st.session_state.simulation_started = True

    add_event(
        f"Simulation run {run_number} completed. "
        "City indicators updated."
    )


if reset_clicked:
    reset_simulation()


stats = st.session_state.city_stats


# City statistics
st.subheader("City statistics")

metric_columns = st.columns(3)

metrics = [
