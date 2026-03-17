import streamlit as st
import pandas as pd
import sqlite3
import ollama
import plotly.express as px
import re

st.set_page_config(page_title="Talk to Data AI", layout="wide")

st.title("📊 DataPilot AI (LLM Local'OLLAMA model')")

# Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Upload Dataset
file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if file:

    df = pd.read_csv(file, encoding="cp1252")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Create SQLite Database
    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, if_exists="replace", index=False)

    # Ask Question
    question = st.text_input("Ask a question about your data")

    if question:

        prompt = f"""
You are a SQL expert.

Convert the question into a SQLite SQL query.

Rules:
- Return ONLY SQL query
- No explanation
- No markdown
- Table name: data
- Columns: {list(df.columns)}

Question: {question}
"""

        with st.spinner("Generating SQL..."):

            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            sql_query = response["message"]["content"]

        # Clean SQL
        sql_query = re.sub(r"```sql|```", "", sql_query).strip()

        if "SELECT" in sql_query:
            sql_query = sql_query[sql_query.index("SELECT"):]

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        # Execute Query
        try:

            result = pd.read_sql_query(sql_query, conn)

            st.subheader("Query Result")
            st.dataframe(result)

            # Save history
            st.session_state.history.append({
                "question": question,
                "sql": sql_query
            })

            # Visualization Section
            st.subheader("📈 Data Visualization")

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

                numeric_cols = result.select_dtypes(include=["int64","float64"]).columns
                all_cols = result.columns

                x = st.selectbox("Select X Axis", all_cols)

                if chart_type != "Histogram":
                    y = st.selectbox("Select Y Axis", numeric_cols)

                if chart_type == "Bar Chart":
                    fig = px.bar(result, x=x, y=y, title="Bar Chart")

                elif chart_type == "Line Chart":
                    fig = px.line(result, x=x, y=y, title="Line Chart")

                elif chart_type == "Pie Chart":
                    fig = px.pie(result, names=x, values=y, title="Pie Chart")

                elif chart_type == "Scatter Plot":
                    fig = px.scatter(result, x=x, y=y, title="Scatter Plot")

                elif chart_type == "Histogram":
                    fig = px.histogram(result, x=x, title="Histogram")

                elif chart_type == "Box Plot":
                    fig = px.box(result, x=x, y=y, title="Box Plot")

                elif chart_type == "Area Chart":
                    fig = px.area(result, x=x, y=y, title="Area Chart")

                elif chart_type == "Heatmap":
                    corr = result.corr(numeric_only=True)
                    fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# Query History
if st.session_state.history:

    st.sidebar.title("🕘 Query History")

    for item in st.session_state.history[::-1]:
        st.sidebar.write("**Question:**", item["question"])
        st.sidebar.code(item["sql"])