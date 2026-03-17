# 📊 Automatic SQL Query Generator with Visualization

## 🚀 Overview

This project is an AI-powered data analysis tool that allows users to interact with their datasets using natural language. It leverages a local Large Language Model (LLM) to automatically convert user queries into SQL, execute them, and visualize the results.

---

## 🧠 Supported LLM Models

Download and run any one of the following models using Ollama:

* llama3
* qwen:1.7b
* gemma2

---

## ⚙️ Installation & Setup

### 1. Install Ollama

Run the following command in your command prompt:

```
pip install ollama
```

---

### 2. Download a Model

You can pull any one model:

```
ollama pull llama3
```

OR

```
ollama pull qwen:1.7b
```

---

### 3. Configure the Model

* Open `app.py`
* Ensure the model name matches the one you downloaded

Example:

```python
model = "llama3"
```

---

### 4. Run the Application

Navigate to your project folder and run:

```
streamlit run app.py
```

---

## 📂 How to Use

1. Upload a CSV file through the Streamlit interface
2. Enter your question in natural language (e.g., "Top 5 countries by sales")
3. The system will:

   * Convert your question into an SQL query
   * Execute the query on the dataset
   * Display results in table format
   * Generate visualizations automatically

---

## 📊 Features

* Natural Language to SQL conversion
* Local LLM (no API required)
* Automatic data visualization
* Supports CSV datasets
* Interactive UI using Streamlit

---

## 🧩 Workflow

User Question
↓
Streamlit Interface
↓
LLM (Ollama Model)
↓
Text → SQL Conversion
↓
SQL Execution
↓
Pandas DataFrame
↓
Visualization (Plotly)

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Ollama (Local LLM)
* Pandas
* SQLite
* Plotly

---

## ✅ Use Cases

* Quick data analysis without SQL knowledge
* Business insights generation
* Exploratory Data Analysis (EDA)
* Student and learning projects

---

## 📌 Notes

* Ensure the model is running before starting the app
* Use clean and structured CSV files for best results
* Modify prompts for more accurate SQL generation

---

## 🎯 Conclusion

This project simplifies data analysis by combining AI and visualization. Users can easily explore datasets, generate insights, and understand trends without writing complex SQL queries.

---
