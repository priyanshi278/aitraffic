import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Traffic & Transport Intelligence System",
    page_icon="🚦",
    layout="centered"
)

st.title("🚦 AI Traffic & Transport Intelligence System")


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Route Analysis", "Create Route"])

if page == "Route Analysis":
    st.caption("Decision Support for Smart Route Selection")


    st.subheader("Route Analysis")

    start_location = st.text_input("Start Location",placeholder="e.g. Alambagh")

    end_location = st.text_input("End Location",placeholder="e.g. Gomti Nagar")

    analyze_btn = st.button("Analyze Best Route")



    if analyze_btn:
        if not start_location or not end_location:
            st.warning("Please enter both start and end locations.")
        else:
            with st.spinner("Analyzing traffic and incidents..."):
                try:
                    response = requests.get(
                        f"{BASE_URL}/analysis/route",
                        params={
                            "start_location": start_location,
                            "end_location": end_location
                        },
                        timeout=15
                    )
                    

                    if response.status_code != 200:
                        st.error("Failed to fetch analysis from server.")
                    else:
                        data = response.json()
                        print(data["routes_analysis"])
                        st.subheader("📊 All Routes Analysis")

                        df = pd.DataFrame(data["routes_analysis"])
                        df = df[[
                            "via",
                            "avg_time_min",
                            "incident_count",
                            "congestion_level",
                            "score"
                        ]]

                        st.dataframe(
                            df.style.format({"score": "{:.2f}"}),
                            use_container_width=True,
                        )

                        st.subheader("🧮 Rule-Based Route Decision")

                        st.subheader("Recommended Route")
                        st.success(data["rule_based_decision"]["recommended_route"])

                        st.subheader("Why this route?")
                        st.info(data["rule_based_decision"]["explanation"])
                    

                        st.subheader("AI Recommendation")

                        if data["ai_decision"]["available"]:
                            st.write(data["ai_decision"]["summary"])
                        else:
                            st.warning(data["ai_decision"]["summary"])



                except Exception as e:
                    st.error(f"Server error: {e}")
if page == "Create Route":

    st.subheader("Add New Route")
    start = st.text_input("Start Location")
    end = st.text_input("End Location")
    via = st.text_input("Via Locations")
    distance = st.number_input("Distance (km)", min_value=0.0, step=0.1)
    avg_time = st.number_input("Average Time (min)", min_value=0.0, step=0.1)

    if st.button("Add Route"):
        payload = {
            "start_location": start,
            "end_location": end,
            "via_locations": via,
            "distance_km": distance,
            "average_time_min": avg_time
        }
        res = requests.post(f"{BASE_URL}/routes/routes/", json=payload)

        st.write("Status code:", res.status_code)
        st.write("Response:", res.text)
        if res.status_code in (200, 201):
            st.success("✅ Route added successfully!")
        else:
            st.error(f"❌ Failed to add route: {res.text}")

