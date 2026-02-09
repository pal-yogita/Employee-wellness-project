# 🧠 Employee Wellness Interactive Dashboard

An interactive web application built with Flask and Plotly to analyze and present insights from the Employee Mental Health in Tech survey. This project transforms a raw dataset into a dynamic, presentation-ready dashboard designed to uncover key factors affecting employee wellness.

---
## ✨ Key Features

* **Interactive Visualizations**: Uses Plotly to create beautiful, responsive charts that allow for data exploration.
* **Presentation-Focused UI**: The user interface is designed as a "presentation lobby," with 6 distinct topics corresponding to different presenters.
* **Dynamic Content**: Built with a Flask backend that processes data and serves insights dynamically.
* **Staggered Animations**: Smooth, scroll-based animations to reveal insights and charts in a professional, engaging manner.
* **Clean & Modern Design**: A custom style guide with a professional color palette and typography for a polished user experience.

---
## 📸 Screenshot


*The homepage serves as a "presentation lobby," allowing users to navigate to different sections of the analysis.*

---
## 🛠️ Technology Stack

* **Backend**: Python, Flask
* **Data Analysis**: Pandas
* **Interactive Charting**: Plotly
* **Frontend**: HTML, Bootstrap 5, Custom CSS
* **Animations**: JavaScript (IntersectionObserver API)

---
## 📁 Project Structure

```

employee\_wellness\_project/
├── app.py                      \# Main Flask application
├── analysis.py                 \# Data analysis & Plotly functions
├── cleaned\_employee\_data.csv   \# The cleaned, ready-to-use data
├── requirements.txt            \# Project dependencies
├── templates/
│   ├── layout.html             \# Base template (navbar, footer)
│   ├── index.html              \# Homepage / Presentation Lobby
│   └── presenter\_dashboard.html \# Reusable dashboard template
└── static/
├── css/
│   └── style.css           \# Custom styles and animations
└── js/
└── animations.js       \# Scroll animation logic

````

---
## 🚀 Setup and Installation Guide

Follow these steps to run the project on your local machine.

### **Prerequisites**

* Python 3.8+
* pip (Python package installer)

### **Installation Steps**

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone [your-repository-link]
    cd employee_wellness_project
    ```

2.  **Create and activate a virtual environment** (Recommended):
    * **On macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies** using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application**:
    ```bash
    python app.py
    ```

5.  **Access the application**:
    * Once the server is running, you will see a message in the terminal like:
        `* Running on http://127.0.0.1:5000`
    * Open your web browser and navigate to this URL to see the application live.
