import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Electricity Consumption Analyzer",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #00BFFF;
    color: white;
    font-size: 16px;
}

.metric-box {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Smart Electricity Consumption Analyzer")
st.markdown(
    "Analyze household electricity usage, estimate monthly bills, "
    "and track appliance-wise consumption."
)

st.sidebar.header("🏠 User Information")

name = st.sidebar.text_input("Enter Your Name")
city = st.sidebar.text_input("Enter City")

house_type = st.sidebar.selectbox(
    "Select House Type",
    ["1BHK", "2BHK", "3BHK"]
)

tariff = st.sidebar.slider(
    "Electricity Rate (₹ per kWh)", 1, 15, 5)

st.header("📌 Appliance Usage Per Day")

appliances = {
    "Air Conditioner": 1.5,
    "Fan": 0.07,
    "Television": 0.1,
    "Refrigerator": 0.15,
    "Washing Machine": 0.5,
    "Laptop": 0.06,
    "Lights": 0.04
}

usage_data = []

col1, col2 = st.columns(2)

for i, (appliance, power) in enumerate(appliances.items()):

    with col1 if i % 2 == 0 else col2:

        hours = st.slider(
            f"{appliance} Usage Hours", 0, 24, 2)

        daily_consumption = power * hours

        usage_data.append({
            "Appliance": appliance,
            "Power Rating (kW)": power,
            "Hours Used": hours,
            "Daily Consumption (kWh)": round(daily_consumption, 2)
        })

df = pd.DataFrame(usage_data)

# Calculate Button
if st.button("⚡ Calculate Electricity Consumption"):

    if name and city:

        total_daily = df["Daily Consumption (kWh)"].sum()

        monthly_consumption = total_daily * 30

        estimated_bill = monthly_consumption * tariff

        carbon_footprint = monthly_consumption * 0.82

        st.header("📊 Consumption Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Daily Consumption",
                f"{total_daily:.2f} kWh"
            )

        with c2:
            st.metric(
                "Monthly Consumption",
                f"{monthly_consumption:.2f} kWh"
            )

        with c3:
            st.metric(
                "Estimated Bill",
                f"₹{estimated_bill:.2f}"
            )

        # User Information
        st.header("👤 User Information")

        st.info(f"""
        **Name:** {name}

        **City:** {city}

        **House Type:** {house_type}

        **Electricity Rate:** ₹{tariff}/kWh
        """)
        st.header("📋 Appliance Usage Table")

        st.dataframe(df, use_container_width=True)

        st.header("🥧 Appliance-wise Energy Consumption")

        pie_chart = px.pie(
            df,
            values="Daily Consumption (kWh)",
            names="Appliance",
            hole=0.4
        )

        st.plotly_chart(pie_chart, use_container_width=True)

        st.header("📈 Daily Consumption Analysis")

        bar_chart = px.bar(
            df,
            x="Appliance",
            y="Daily Consumption (kWh)",
            text="Daily Consumption (kWh)"
        )

        st.plotly_chart(bar_chart, use_container_width=True)

        # Highest Consumption Appliance
        highest = df.loc[
            df["Daily Consumption (kWh)"].idxmax()
        ]

        st.warning(
            f"⚠ Highest Electricity Consumption: "
            f"{highest['Appliance']} "
            f"({highest['Daily Consumption (kWh)']} kWh/day)"
        )

        st.success(
            f"🌍 Estimated Carbon Footprint: "
            f"{carbon_footprint:.2f} kg CO₂/month"
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Report",
            data=csv,
            file_name="electricity_report.csv",
            mime="text/csv"
        )

        st.header("💡 Energy Saving Tips")

        tips = [
            "Use LED bulbs instead of CFL bulbs.",
            "Turn off appliances when not in use.",
            "Use energy-efficient 5-star appliances.",
            "Keep AC temperature at 24°C.",
            "Unplug chargers after usage."
        ]

        for tip in tips:
            st.write("✅", tip)

    else:
        st.error("Please enter Name and City.")
