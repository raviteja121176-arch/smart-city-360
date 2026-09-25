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
    "Emergency": (
        "Emergency services",
        "View the locations of the Hospital, Police Station, and Fire Station on the city map.",
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
            "message": "City data reset to the starting values.",
        }
    ]


st.set_page_config(
    page_title="Smart City 360",
    page_icon="🏙️",
    layout="wide",
)

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

st.sidebar.title("Smart City 360")
st.sidebar.caption("CITY OPERATIONS")
selected_section = st.sidebar.radio("Navigate", SECTIONS)
st.sidebar.divider()
st.sidebar.caption("DEMO CITY")
st.sidebar.write("Greenfield")

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
        reset_clicked = st.button("Reset", use_container_width=True)

    if start_clicked:
        stats = st.session_state.city_stats
        run_number = st.session_state.simulation_runs + 1

        stats["traffic"] = max(36, stats["traffic"] - 4)
        stats["energy"] = min(94, stats["energy"] + 2)
        stats["water"] = min(98, stats["water"] + 1)
        stats["waste"] = min(94, stats["waste"] + 2)
        stats["air_quality"] = max(20, stats["air_quality"] - 3)

        st.session_state.simulation_runs = run_number
        st.session_state.simulation_started = True
        add_event(f"Simulation run {run_number} completed. City indicators updated.")

    if reset_clicked:
        reset_simulation()

if st.session_state.simulation_started:
    st.sidebar.success("Simulation active")
else:
    st.sidebar.info("Simulation ready")

stats = st.session_state.city_stats

st.subheader("City statistics")
metric_columns = st.columns(3)

metrics = [
    ("Population", f"{stats['population'] / 1_000_000:.2f}M"),
    ("Traffic · congestion", f"{stats['traffic']}%"),
    ("Energy · renewable share", f"{stats['energy']}%"),
    ("Water · service coverage", f"{stats['water']}%"),
    ("Waste · recycled", f"{stats['waste']}%"),
    ("Air Quality Index", str(stats["air_quality"])),
]

for index, (label, value) in enumerate(metrics):
    with metric_columns[index % 3]:
        st.metric(label, value)

if selected_section == "Traffic":
    st.subheader("Traffic Management Center")
    st.write("Simulate a traffic event and see how the city responds.")

    traffic_event = st.selectbox(
        "Select a traffic event",
        list(TRAFFIC_EVENTS.keys()),
    )

    event_info = TRAFFIC_EVENTS[traffic_event]

    preview_column, response_column = st.columns([1, 2])

    with preview_column:
        st.metric("Current congestion", f"{stats['traffic']}%")

    with response_column:
        st.info(
            f"Planned response: {event_info['response']}"
        )

    if st.button(
        "Respond to Traffic Event",
        type="primary",
        use_container_width=True,
    ):
        old_congestion = stats["traffic"]
        old_aqi = stats["air_quality"]

        stats["traffic"] = max(
            20,
            min(95, stats["traffic"] + event_info["congestion"]),
        )

        stats["air_quality"] = max(
            10,
            min(100, stats["air_quality"] + event_info["aqi"]),
        )

        st.session_state.simulation_started = True

        add_event(
            f"{traffic_event}: congestion changed {old_congestion}% → "
            f"{stats['traffic']}%. AQI changed {old_aqi} → {stats['air_quality']}."
        )

        st.success(event_info["response"])

elif selected_section != "Dashboard":
    detail_title, detail_text = SECTION_INFO[selected_section]

    st.subheader(f"{selected_section} overview")

    if selected_section == "Emergency":
        st.info(detail_text)
    else:
        if selected_section == "Energy":
            detail_value = f"{stats['energy']}%"
        elif selected_section == "Water":
            detail_value = f"{stats['water']}%"
        elif selected_section == "Waste":
            detail_value = f"{stats['waste']}%"
        else:
            detail_value = str(stats["air_quality"])

        detail_column, explanation_column = st.columns([1, 3])

        with detail_column:
            st.metric(detail_title, detail_value)

        with explanation_column:
            st.write(detail_text)

st.subheader("Greenfield city map")
st.caption("A simple, fictional layout · not to scale")

map_rows = [
    (
        "NORTH DISTRICT",
        [
            ("SCHOOL", "North Campus"),
            ("PARK", "North Park"),
            ("FIRE STATION", "Station 1"),
        ],
    ),
    (
        "CENTRAL DISTRICT",
        [
            ("HOSPITAL", "Greenfield Medical"),
            ("CITY CENTER", "Central Avenue"),
            ("POLICE STATION", "Central Precinct"),
        ],
    ),
    (
        "SOUTH DISTRICT",
        [
            ("POWER PLANT", "Solar Grid"),
            ("COMMUNITY HUB", "South Square"),
            ("WATER WORKS", "Reservoir Road"),
        ],
    ),
]

for district_name, places in map_rows:
    st.caption(district_name)
    place_columns = st.columns(3)

    for index, (place_name, place_detail) in enumerate(places):
        with place_columns[index]:
            with st.container(border=True):
                st.markdown(f"**{place_name}**")
                st.caption(place_detail)

    st.caption("────────────── Main Avenue ──────────────")

st.subheader("Event Log")

for event in st.session_state.event_log:
    time_column, message_column = st.columns([1, 7])

    with time_column:
        st.caption(event["time"])

    with message_column:
        st.write(event["message"])
