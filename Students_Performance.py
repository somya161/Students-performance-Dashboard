# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 18:52:59 2025

@author: somya
"""

# student_dashboard.py
import streamlit as st
import pandas as pd

# -------------------------
# Load Dataset
# -------------------------
st.title("🎓 Student Performance Dashboard")

# Load the data
df = pd.read_csv("students_data.csv")

# Display the dataset
st.subheader("📋 Complete Student Data")
st.dataframe(df)

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🎛️ Filter Students")

# Select Course
course = st.sidebar.selectbox(
    "Select Course:",
    ["All"] + sorted(df["Course"].unique().tolist())
)

# Select City
city = st.sidebar.multiselect(
    "Select City:",
    sorted(df["City"].unique().tolist())
)

# Gender Filter
gender = st.sidebar.radio(
    "Select Gender:",
    ["All", "Male", "Female"]
)

# Minimum Marks
min_marks = st.sidebar.slider(
    "Minimum Marks:",
    min_value=0,
    max_value=100,
    value=50
)

# -------------------------
# Apply Filters
# -------------------------
filtered_df = df.copy()

if course != "All":
    filtered_df = filtered_df[filtered_df["Course"] == course]

if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]

filtered_df = filtered_df[filtered_df["Marks"] >= min_marks]

# Show filtered data
st.subheader("🎯 Filtered Data")
st.dataframe(filtered_df)

# -------------------------
# Display Summary Metrics
# -------------------------
st.subheader("📊 Summary Statistics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average Marks", round(filtered_df["Marks"].mean(), 2))
col3.metric("Average Attendance (%)", round(filtered_df["Attendance (%)"].mean(), 2))

# -------------------------
# Search by Name
# -------------------------
st.subheader("🔍 Search Student by Name")
search_name = st.text_input("Enter Student Name")

if search_name:
    result = df[df["Name"].str.contains(search_name, case=False, na=False)]
    if not result.empty:
        st.success(f"Found {len(result)} student(s):")
        st.dataframe(result)
    else:
        st.warning("No student found with that name.")

# -------------------------
# Buttons: Top Performers / Show All
# -------------------------
st.subheader("🏅 Actions")

if st.button("Show Top Performers (Marks > 90)"):
    top_students = df[df["Marks"] > 90]
    st.success(f"Showing {len(top_students)} top performers:")
    st.dataframe(top_students)

if st.button("Show All Data"):
    st.info("Displaying all students again.")
    st.dataframe(df)

# -------------------------
# Charts
# -------------------------
st.subheader("📈 Visual Analysis")

chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart (Marks by Student)", "Bar Chart (Average Marks by Course)"]
)

if chart_type == "Bar Chart (Marks by Student)":
    st.bar_chart(filtered_df.set_index("Name")["Marks"])
else:
    avg_marks = df.groupby("Course")["Marks"].mean().sort_values(ascending=False)
    st.bar_chart(avg_marks)

# -------------------------
# Display Messages Based on Performance
# -------------------------
st.subheader("💬 Performance Message")

if filtered_df["Marks"].mean() > 85:
    st.success("Excellent Performance! Keep it up! 💪")
elif filtered_df["Marks"].mean() >= 70:
    st.info("Good Performance. A little more effort can make it great! 👍")
else:
    st.warning("Needs Improvement. Focus more on studies! 📚")


# -------------------------
# End Message
# -------------------------
st.markdown("---")
st.markdown("Created with ❤️ using **Streamlit**")
