# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import re
from groq import Groq

# -----------------------------------
# Streamlit Page Config
# -----------------------------------
st.set_page_config(page_title="Talk to Data AI", layout="wide")

st.title("DataPilot AI")

# -----------------------------------
# GROQ API KEY INPUT
# -----------------------------------
st.sidebar.title("Groq API Configuration")

api_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

# -----------------------------------
# Initialize Groq Client
# -----------------------------------
client = None

if api_key:
    client = Groq(api_key=api_key)

# -----------------------------------
# Session State
# -----------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------
# Upload Dataset
# -----------------------------------
file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if file:

    # Read CSV
    df = pd.read_csv(file, encoding="cp1252")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------------
    # Create SQLite Database
    # -----------------------------------
    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, if_exists="replace", index=False)

    # -----------------------------------
    # Ask Question
    # -----------------------------------
    question = st.text_input("Ask a question about your data")

    if question:

        if not api_key:
            st.warning("Please enter Groq API key")
            st.stop()

        prompt = f"""
You are a SQLite SQL expert.

Convert the user question into a valid SQLite SQL query.

Rules:
- Return ONLY SQL query
- No explanation
- No markdown
- Table name: data
- Columns: {list(df.columns)}

Question: {question}
"""

        # -----------------------------------
        # Generate SQL using Groq
        # -----------------------------------
        with st.spinner("Generating SQL..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            sql_query = response.choices[0].message.content

        # -----------------------------------
        # Clean SQL Query
        # -----------------------------------
        sql_query = re.sub(
            r"```sql|```",
            "",
            sql_query
        ).strip()

        if "SELECT" in sql_query.upper():
            sql_query = sql_query[
                sql_query.upper().index("SELECT"):
            ]

        # -----------------------------------
        # Show SQL Query
        # -----------------------------------
        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        # -----------------------------------
        # Execute SQL Query
        # -----------------------------------
        try:

            result = pd.read_sql_query(sql_query, conn)

            st.subheader("Query Result")
            st.dataframe(result)

            # Save History
            st.session_state.history.append({
                "question": question,
                "sql": sql_query
            })

            # -----------------------------------
            # Visualization Section
            # -----------------------------------
            st.subheader("Data Visualization")

            if len(result.columns) >= 1:

                chart_type = st.selectbox(
                    "Select Chart Type",
                    [
                        "Bar Chart",
                        "Line Chart",
                        "Pie Chart",
                        "Scatter Plot",
                        "Histogram",
                        "Box Plot",
                        "Area Chart",
                        "Heatmap"
                    ]
                )

                numeric_cols = result.select_dtypes(
                    include=["int64", "float64"]
                ).columns

                all_cols = result.columns

                x = st.selectbox(
                    "Select X Axis",
                    all_cols
                )

                y = None

                if (
                    chart_type != "Histogram"
                    and len(numeric_cols) > 0
                ):
                    y = st.selectbox(
                        "Select Y Axis",
                        numeric_cols
                    )

                # -----------------------------------
                # Generate Charts
                # -----------------------------------
                if chart_type == "Bar Chart":
                    fig = px.bar(result, x=x, y=y)

                elif chart_type == "Line Chart":
                    fig = px.line(result, x=x, y=y)

                elif chart_type == "Pie Chart":
                    fig = px.pie(result, names=x, values=y)

                elif chart_type == "Scatter Plot":
                    fig = px.scatter(result, x=x, y=y)

                elif chart_type == "Histogram":
                    fig = px.histogram(result, x=x)

                elif chart_type == "Box Plot":
                    fig = px.box(result, x=x, y=y)

                elif chart_type == "Area Chart":
                    fig = px.area(result, x=x, y=y)

                elif chart_type == "Heatmap":

                    corr = result.corr(
                        numeric_only=True
                    )

                    fig = px.imshow(
                        corr,
                        text_auto=True,
                        title="Correlation Heatmap"
                    )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# -----------------------------------
# Query History
# -----------------------------------
if st.session_state.history:

    st.sidebar.title("Query History")

    for item in st.session_state.history[::-1]:

        st.sidebar.write(
            "**Question:**",
            item["question"]
        )

        st.sidebar.code(item["sql"])
