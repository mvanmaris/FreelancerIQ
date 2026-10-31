# --- IMPORTS ---
import streamlit as st
import altair as alt
from project import (
    load_data,
    calculate_total_cost,
    calculate_minutes_per_unit,
    calculate_cost_per_unit
)


# --- DASHBOARD ---
st.title("FreelanceIQ")
st.write("Freelance Productivity & Cost Dashboard")


# --- LOAD CSV ---
st.write("Upload a CSV file containing your freelancer data.")

st.caption(
    "Required CSV headers: week, freelancer, content_units, hours, hourly_rate. "
    "Column names must match exactly."
)

uploaded_file = st.file_uploader(
    "Upload Freelancer Data",
    type="csv"
)

if uploaded_file is None:
    st.info("Upload a CSV file to get started.")
    st.stop()

try:
    data = load_data(uploaded_file)

except (KeyError, ValueError, UnicodeError):
    st.error(
        "Unable to read the CSV. Please check that your file has the "
        "required headers and contains valid numbers."
    )
    st.stop()


# --- GET UNIQUE FREELANCERS ---
freelancers = set()

for row in data:
    freelancers.add(row["freelancer"])

sorted_freelancers = sorted(freelancers)


# --- GROUP DATA BY FREELANCER ---
freelancer_data = {}

for freelancer in sorted_freelancers:
    freelancer_rows = []

    for row in data:
        if row["freelancer"] == freelancer:
            freelancer_rows.append(row)

    freelancer_data[freelancer] = freelancer_rows


# --- FREELANCER FILTER ---
filter_options = ["All Freelancers"] + sorted_freelancers

selected_freelancer = st.selectbox(
    "Select a Freelancer",
    filter_options
)


# --- FILTER DISPLAYED DATA ---
if selected_freelancer == "All Freelancers":
    selected_rows = data
else:
    selected_rows = freelancer_data[selected_freelancer]


# --- CALCULATE TOTAL SPEND ---
costs = []

for row in selected_rows:
    cost = calculate_total_cost(row["hours"], row["hourly_rate"])
    costs.append(cost)

total_spend = sum(costs)


# --- CALCULATE TOTAL CONTENT UNITS ---
content_units = []

for row in selected_rows:
    content_units.append(row["content_units"])

total_units = sum(content_units)


# --- CALCULATE TOTAL HOURS ---
hours = []

for row in selected_rows:
    hours.append(row["hours"])

total_hours = sum(hours)

# --- CALCULATE OVERALL PRODUCTIVITY ---
overall_minutes_per_unit = calculate_minutes_per_unit(total_hours, total_units)
if overall_minutes_per_unit is None:
    overall_minutes_display = "N/A"
else:
    overall_minutes_display = f"{overall_minutes_per_unit:.2f}"


# --- CALCULATE COST PER UNIT ---
overall_cost_per_unit = calculate_cost_per_unit(total_spend, total_units)

if overall_cost_per_unit is None:
    overall_cost_display = "N/A"
else:
    overall_cost_display = f"${overall_cost_per_unit:.2f}"
# --- DISPLAY KPIs ---

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Freelancer Spend", f"${total_spend:,.2f}")

with col2:
    st.metric("Total Content Units", f"{total_units:,}")

with col3:
    st.metric("Total Freelancer Hours", f"{total_hours:.1f}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Overall Minutes per Unit", overall_minutes_display)

with col5:
    st.metric("Cost per Unit", overall_cost_display)


# --- FREELANCER COMPARISON ---
st.header("Freelancer Comparison")

productivity_data = {}
cost_data = {}

for freelancer in sorted_freelancers:
    freelancer_rows = freelancer_data[freelancer]

    total_freelancer_hours = 0
    total_freelancer_units = 0
    total_freelancer_cost = 0

    for row in freelancer_rows:
        total_freelancer_hours += row["hours"]
        total_freelancer_units += row["content_units"]

        cost = calculate_total_cost(row["hours"], row["hourly_rate"])
        total_freelancer_cost += cost

    minutes_per_unit = calculate_minutes_per_unit(
        total_freelancer_hours,
        total_freelancer_units
    )

    cost_per_unit = calculate_cost_per_unit(
        total_freelancer_cost,
        total_freelancer_units
    )

    if minutes_per_unit is not None:
        productivity_data[freelancer] = minutes_per_unit

    if cost_per_unit is not None:
        cost_data[freelancer] = cost_per_unit


# --- PRODUCTIVITY CHART ---
st.write("**Productivity - Minutes per Content Unit**")
st.caption("Lower values indicate faster production.")

sorted_productivity = dict(
    sorted(productivity_data.items(), key=lambda item: item[1])
)

productivity_rows = []

for freelancer, minutes in sorted_productivity.items():
    productivity_rows.append({
        "Freelancer": freelancer,
        "Minutes per Unit": minutes
    })

productivity_chart = alt.Chart(
    alt.Data(values=productivity_rows)
).mark_bar().encode(
    x=alt.X("Minutes per Unit:Q", title="Minutes per Unit"),
    y=alt.Y("Freelancer:N", sort="x", title="Freelancer"),
    color=alt.condition(
        alt.datum.Freelancer == selected_freelancer,
        alt.value("#067A46"),
        alt.value("#8BC2AA")
    ),
    tooltip=["Freelancer:N", "Minutes per Unit:Q"]
)

st.altair_chart(productivity_chart, use_container_width=True)


# --- COST-EFFECTIVENESS CHART ---
st.write("**Cost-Effectiveness - Cost per Content Unit**")
st.caption("Lower values indicate lower production costs.")

sorted_cost = dict(
    sorted(cost_data.items(), key=lambda item: item[1])
)

cost_rows = []

for freelancer, cost in sorted_cost.items():
    cost_rows.append({
        "Freelancer": freelancer,
        "Cost per Unit": cost,
    })

cost_chart = alt.Chart(
    alt.Data(values=cost_rows)
).mark_bar().encode(
    x=alt.X("Cost per Unit:Q", title="Cost per Unit ($)"),
    y=alt.Y("Freelancer:N", sort="x", title="Freelancer"),
    color=alt.condition(
        alt.datum.Freelancer == selected_freelancer,
        alt.value("#067A46"),
        alt.value("#8BC2AA")
    ),
    tooltip=["Freelancer:N", "Cost per Unit ($):Q"]
)

st.altair_chart(cost_chart, use_container_width=True)

# --- DISPLAY FILTERED DATA ---
st.subheader("Freelancer Data")
st.dataframe(selected_rows)



